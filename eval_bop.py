import yaml
import numpy
import calibur
from typing import Dict

def arr2str(x: numpy.ndarray):
    return ' '.join(map(str, x.reshape(-1).tolist()))


x: Dict[object, Dict[object, dict]] = yaml.safe_load(open("debug/industrial_res.yml"))
with open("fp_industrial-test.csv", "w") as fo:
    fo.write("scene_id,im_id,obj_id,score,R,t,time\n")
    for video_id in x.keys():
        for frame_id in x[video_id].keys():
            for obj_id in x[video_id][frame_id]:
                pose = numpy.array(x[video_id][frame_id][obj_id])
                # pose = numpy.linalg.inv(calibur.convert_pose(numpy.linalg.inv(pose), calibur.CC.GL, calibur.CC.CV))
                r = pose[:3, :3]
                t = pose[:3, 3] * 1000
                fo.write(f"{int(video_id)},{int(frame_id)},{int(obj_id)},1.0,{arr2str(r)},{arr2str(t)},1.0\n")
