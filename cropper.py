import subprocess
import os,cv2
import argparse, os, random
import multiprocessing as mp
from multiprocessing import Manager
import logging,sys
from itertools import islice
logging.basicConfig(level=logging.INFO)  # configure logging level to INFO
parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--num_workers', 
                    default=1, 
                    type=int,
                    help="Multi-thread to facilate cropping process")
parser.add_argument('--save_dir', 
                    default='data', 
                    type=str,
                    help="where to save files")
parser.add_argument('--timestamp_dir', 
                    default='./', 
                    type=str,
                    help="save path of timestamps")
parser.add_argument('--video_dir', 
                    default='videos', 
                    type=str,
                    help="save path of videos")
parser.add_argument('--mode', 
                    default='test', 
                    type=str,
                    help="Please Select your Cropping Mode, {full, clean, test}")
args = parser.parse_args()

def process_video_with_detections(input_path, video_output_path,audio_output_path, start_frame,end_frame, detections):
    # 使用OpenCV处理视频
    cap = cv2.VideoCapture(input_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_output_path, fourcc,fps, (112, 112))
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    for idx in range(start_frame, end_frame + 1):
        ret, frame = cap.read()
        if ret:
            x, y, w, h = detections[idx - start_frame]
            cropped_frame = frame[y:y+h, x:x+w]
            resized_frame = cv2.resize(cropped_frame, (112, 112))
            out.write(resized_frame)
    cap.release()
    out.release()
    # 计算音频的起始和结束时间（单位为秒）
    start_time = start_frame / fps
    end_time = end_frame / fps

    # 使用ffmpeg提取特定时间范围的音频为wav格式, 采样率为16000Hz
    cmd = [
        'ffmpeg', '-i', input_path, 
        '-ss', str(start_time), '-to', str(end_time),
        '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', 
        audio_output_path,'-y'
    ]
    subprocess.call(cmd)

def split_dict(data, num_splits):
    keys = list(data.keys())
    random.shuffle(keys)
    split_keys = [keys[i::num_splits] for i in range(num_splits)]
    return [{k: data[k] for k in subset} for subset in split_keys]

def prepare_timestamp(filename):
    bboxes = []
    fns = []
    with open(filename, 'r') as file:
        for line in islice(file, 5, None):  # Starts reading from the 6th line
            [fn,x,y,w,h] = line.strip().split("\t")
            bboxes.append((int(x),int(y),int(w),int(h)))
            fns.append(int(fn))
    return bboxes,fns[0],fns[-1]

def crop_by_spks(spk2videos):
    for spk, videos in spk2videos.items():
        tsf_spk = os.path.join(args.timestamp_dir,spk)
        if not os.path.exists(tsf_spk):
            logging.info(f"Spk dir {tsf_spk} of timestamp does not exist. Skipping...")
            continue
        os.makedirs(os.path.join(args.save_dir,"audio",spk),exist_ok=True)
        os.makedirs(os.path.join(args.save_dir,"video",spk),exist_ok=True)
        for video in videos:
            tsf_video = os.path.join(tsf_spk, video)
            video_path = os.path.join(args.video_dir,spk,video+'.mp4')
            if not os.path.exists(tsf_video):
                logging.info(f"Video dir {tsf_video} of timestamp does not exist. Skipping...")
                continue
            if not os.path.exists(video_path):
                logging.info(f"Video {video_path} does not exist. Skipping...")
                continue
            os.makedirs(os.path.join(args.save_dir,"audio",spk,video),exist_ok=True)
            os.makedirs(os.path.join(args.save_dir,"video",spk,video),exist_ok=True)
            for tsf in os.listdir(tsf_video):
                num = tsf.replace(".txt","")
                ts = os.path.join(tsf_video,tsf)
                bboxes,start,end = prepare_timestamp(ts)

                save_audio_path = os.path.join(args.save_dir,"audio",spk,video,num+".wav")
                save_video_path = os.path.join(args.save_dir,"video",spk,video,num+".avi")
                process_video_with_detections(
                        video_path,save_video_path,save_audio_path, start, end, bboxes)
                

if __name__ == '__main__':
    print("*"*15)
    print("* Cropping Starts *")
    print("*"*15)
    os.makedirs(args.save_dir,exist_ok=True)
    os.makedirs(os.path.join(args.save_dir,"audio"),exist_ok=True)
    os.makedirs(os.path.join(args.save_dir,"video"),exist_ok=True)
    spk2videos_loc = "resource/video_list/spk2videos_%s"%args.mode
    if not os.path.exists(spk2videos_loc):
        logging.error("Video list not exist!!")
        sys.exit()
    spk2videos = {line.split()[0]:line.strip().split()[1:] for line in open(spk2videos_loc)}
    workers = min(args.num_workers,len(spk2videos))
    spk2videos_slices = split_dict(spk2videos,workers)
    pool = mp.Pool(processes=workers)
    pool.map(crop_by_spks, spk2videos_slices)
        # pool.apply(download_by_ids(slices[i]))
    pool.close()
    pool.join() 

    # 使用示例
    