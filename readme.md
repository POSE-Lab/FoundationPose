## Data preparation

1) Download all network weights from [here](https://drive.google.com/drive/folders/1DFezOAD0oD1BblsXVxqDsl8fj0qzB82i?usp=sharing) and put them under the folder `weights/`. For the refiner, you will need `2023-10-28-18-33-37`. For scorer, you will need `2024-01-11-20-02-45`.

1) [Download demo data](https://drive.google.com/drive/folders/1pRyFmxYXmAnpku7nGRioZaKrVJtIsroP?usp=sharing) and extract them under the folder `demo_data/`

1) [Optional] Download our large-scale training data: ["FoundationPose Dataset"](https://drive.google.com/drive/folders/1s4pB6p4ApfWMiMjmTXOFco8dHbNXikp-?usp=sharing)

1) [Optional] Download our preprocessed reference views [here](https://drive.google.com/drive/folders/1PXXCOJqHXwQTbwPwPbGDN9_vLVe0XpFS?usp=sharing) in order to run model-free few-shot version.

# Env setup with docker:
  ```
  cd docker/
  docker pull shingarey/foundationpose_custom_cuda121:latest
  ```

  Then run:

  ```
  xhost +  && docker run --gpus all --env NVIDIA_DISABLE_REQUIRE=1 -it --network=host --name foundationpose  --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -v __PATH_TO_FOUNDATIONPOSE_ON_HOST_PC__:__PATH_ON_CONTAINER__ -v /mnt:/mnt -v /tmp/.X11-unix:/tmp/.X11-unix -v /tmp:/tmp  --ipc=host -e DISPLAY=${DISPLAY} -e GIT_INDEX_FILE foundationpose:latest bash
  ```
  
  Where:
  ```__PATH_TO_FOUNDATIONPOSE_ON_HOST_PC__```  - is the path to the directory on your host system

  ```__PATH_ON_CONTAINER__``` - where to mount inside the container, e.g. /home/your_name

Later you can execute into the container without re-build.
```
docker exec -ai foundationpose bash
```

## Run model-based demo

The paths have been set in argparse by default. If you need to change the scene, you can pass the args accordingly. By running on the demo data, you should be able to see the robot manipulating the mustard bottle. Pose estimation is conducted on the first frame, then it automatically switches to tracking mode for the rest of the video. The resulting visualizations will be saved to the debug_dir specified in the argparse. (Note the first time running could be slower due to online compilation)

## Run on public datasets (LINEMOD, YCB-Video)

For this you first need to download the BOP datasets in /BOP directory.

Export the BOP_DIR:

```
export BOP_DIR=/path/to/your/workspace/FoundationPose/BOP
```

To run the model-based version on any BOP dataset, run:

```
python run_linemod.py --dataset_dir /path/to/BOP/datatset --use_reconstructed_mesh 0
```

The results will be saved to /debug folder.

To run model-free few-shot version. You first need to train Neural Object Field. ref_view_dir is based on where you download in the above "Data prepare" section. Set the dataset flag to your interested dataset.

```
python bundlesdf/run_nerf.py --ref_view_dir /mnt/9a72c439-d0a7-45e8-8d20-d7a235d02763/DATASET/YCB_Video/bowen_addon/ref_views_16 --dataset ycbv
```

Then run the similar command as the model-based version with some small modifications. Here we are using YCB-Video as example:

```
python run_ycb_video.py --ycbv_dir /mnt/9a72c439-d0a7-45e8-8d20-d7a235d02763/DATASET/YCB_Video --use_reconstructed_mesh 1 --ref_view_dir /mnt/9a72c439-d0a7-45e8-8d20-d7a235d02763/DATASET/YCB_Video/bowen_addon/ref_views_16
```

## Evaluation

FoundationPose creates a .yaml file inside the debug directory. Run eval_bop.py after changing the necessary paths to create the BOP submission csv. You can then use BOP toolkit for the evaluation.