# The VoxBlink Dataset

The VoxBlink dataset is a Large Scale speaker verification dataset obtained from YouTube platform. This repository provides guidelines some scripts for building the corpus with the annotation files. For more introduction, please see [cite](https://VoxBlink.github.io). 

## Resource 
Let's start with obtaining the [resource](https://drive.google.com/drive/folders/1vP8hyT_Zefj2d40JzHLAUJWy_dBjpA22?usp=drive_link) files and decompressing tar-files.
```bash
tar -zxvf timestamp.tar.gz
tar -zxvf video_tags.tar.gz 
```

## File structure


```
% The file structure is summarized as follows: 
|---- resource                  # resource folder
|     |---- data               # [utt] spkid-videoid-uttid
|           |---- utt_clean	
|           |---- utt_full	
|     |---- meta             # meta-data：
|           |---- spk2gender	# [spkid,gender] speaker gender labels
|           |---- spk2lan	# [spkid,language] speaker language labels
|           |---- spk2loc	# [spkid,location] speaker location labels
|           |---- utt2dur	# [utt]
|     |---- timestamp		# timestamps for video/audio cropping
|           |---- id00000	# spkid
|                 |---- DwgYRqnQZHM	#videoid
|                       |---- 00000.txt	#uttid
|                       |---- ...
|                 |---- ... 
|           |---- ...	
|     |---- video_list [spk videoid1 videoid2 ...] list for downloading videos
|           |---- spk2videos_clean	# voxblink-clean video list (18k+ speakers)
|           |---- spk2videos_full	# voxblink video list (38k+ speakers)
|           |---- spk2videos_test	# video list for testing scripts
|     |---- video_tags
|           |---- id00000.txt
|           |---- id00001.txt
|           |---- ...


|---- cropper.py	# extract speech/video segments by timestamps from downloaded videos
|---- downloader.py	# download videos by video_list
|---- LICENSE		# license
|---- README.md	
|---- requirement.txt			

```
## Download
The following procedures show how to construct your VoxBlink
### Pre-requisites
* Install **ffmpeg**:
```bash
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install ffmpeg
```
* Clone Repo:
```bash
git clone https://github.com/VoxBlink/ScriptsForVoxBlink.git
```
* Install Python library:
```bash
python3 -m pip install -r requirements.txt
```

* Download videos

	We provide three modes for you to download videos. We Also leverage multi-thread to facilate download process

	- full: Download VoxBlink complete version.
	
	- clean: Download VoxBlink-clean version.
	
	- test: Test whether the scripts are runnable.

```python
python downloader.py --base_dir $BASE_DIR$ --num_workers 4 --mode full
```

* Crop Videos
	
```python
python cropper.py --save_dir data/ --timestamp_dir resource/timestamp --num_workers 4 --mode test --video_dir $BASE_DIR$
```

## License

The dataset is licensed under the **CC BY-NC-SA 4.0** license. This means that you can share and adapt the dataset for non-commercial purposes as long as you provide appropriate attribution and distribute your contributions under the same license. Detailed terms can be found [here](LICENSE).

Important Note: Our released dataset only contains annotation data, including the YouTube links, time stamps and speaker labels. We do not release audio or visual data and it is the user's responsibility to decide whether and how to download the video data and whether their intended purpose with the downloaded data is legal in their country.. For YouTube users with concerns regarding their videos' inclusion in our dataset, please contact us via E-mail: yuke.lin@dukekunshan.edu.cn or ming.li369@dukekunshan.edu.cn.




## Citation

Please cite the paper below if you make use of the dataset:

```
@INPROCEEDINGS{10446780,
  author={Lin, Yuke and Qin, Xiaoyi and Zhao, Guoqing and Cheng, Ming and Jiang, Ning and Wu, Haiying and Li, Ming},
  booktitle={ICASSP 2024 - 2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)}, 
  title={Voxblink: A Large Scale Speaker Verification Dataset on Camera}, 
  year={2024},
  volume={},
  number={},
  pages={10271-10275},
  keywords={Training;Video on demand;Purification;Pipelines;Signal processing;Web sites;Noise measurement;Speaker Verification;Dataset;Large-scale;Multi-modal},
  doi={10.1109/ICASSP48485.2024.10446780}}

```