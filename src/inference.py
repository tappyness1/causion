from peekingduck.pipeline.nodes.model import yolo as pkd_yolo
import cv2
from collections import defaultdict
import numpy as np
import json
from skimage.draw import polygon

def get_counts(inference_outputs):
    """helper function to count the objects belonging to each class

    Args:
        inference_outputs (_type_): _description_

    Returns:
        counts_dict (dictionary): counts of each class
    """

    counts_dict = defaultdict(int)

    for item in inference_outputs["bbox_labels"]:
        counts_dict[item] += 1

    # fill in missing keys and set their number to zero
    missing_keys = [item for item in ["car", "motorcycle", "motorbike" "truck", "bus"] if item not in counts_dict.keys()]
    
    for key in missing_keys:
        counts_dict[key] = 0

    return dict(counts_dict)

# def get_segmentations(vertices_dict, img, text):
#     print (text)
#     xs = vertices_dict[text]['all_points_x']
#     ys = vertices_dict[text]['all_points_y']
#     vertices = np.array(list(zip(xs, ys)))

#     img = cv2.imread("data/View_from_Second_Link_at_Tuas.jpg")
#     masked = np.zeros((img.shape[0], img.shape[1]), 'uint8')
#     rr, cc = polygon(vertices[:,1], vertices[:,0], img.shape)
#     masked[rr,cc] = 1

#     img_masked_sg = np.where(masked[:,:, None] == 0, img * 0, img)
#     img_masked_jh = np.where(masked[:,:, None] == 0, img, img * 0)

#     return img_masked_sg, img_masked_jh

def get_vertices_dict(polygons):
    vertices_dict = {}

    for k, v in polygons['_via_img_metadata'].items():
        text = v['filename'][:-4]
        # print (v['regions'][0]['shape_attributes']['all_points_x'])
        vertices_dict[text] = {'all_points_x': v['regions'][0]['shape_attributes']['all_points_x'],
                            'all_points_y': v['regions'][0]['shape_attributes']['all_points_y']
        }

    # print (vertices_dict)
    return vertices_dict

class inference:

    def __init__(self):
        self.yolo_node = pkd_yolo.Node(model_type = "v4", detect= ["car", "motorcycle", "truck", "bus"])
        json_file = open("data/shapes_to_sg_only.json")
        polygons = json.load(json_file)

        self.vertices_dict = get_vertices_dict(polygons)

    def get_segmentations(self, img, text):
        xs = self.vertices_dict[text]['all_points_x']
        ys = self.vertices_dict[text]['all_points_y']
        vertices = np.array(list(zip(xs, ys)))

        masked = np.zeros((img.shape[0], img.shape[1]), 'uint8')
        rr, cc = polygon(vertices[:,1], vertices[:,0], img.shape)
        masked[rr,cc] = 1

        img_masked_sg = np.where(masked[:,:, None] == 0, img * 0, img)
        img_masked_jh = np.where(masked[:,:, None] == 0, img, img * 0)

        return img_masked_sg, img_masked_jh
        
    def run_inference(self, img_path):
        """use if img_path is specified 

        Args:
            img_path (_type_): _description_

        Returns:
            _type_: _description_
        """
        image_orig = cv2.imread(img_path)
        image_orig = cv2.cvtColor(image_orig, cv2.COLOR_BGR2RGB)

        yolo_input = {"img": image_orig}
        yolo_output = self.yolo_node.run(yolo_input)
        output_counts_dict = get_counts(yolo_output)

        return output_counts_dict
    
    def run_inference_direct(self, img_bytes, text):
        """use if the img_bytes is specified instead of path

        Args:
            img_bytes (_type_): _description_

        Returns:
            _type_: _description_
        """
        img_decoded = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), -1)
        img_decoded = cv2.cvtColor(img_decoded, cv2.COLOR_BGR2RGB)
        
        img_masked_sg, img_masked_jh = self.get_segmentations(img_decoded, text)
        
        output_counts_dict = {}

        # img_masked_sg 
        # todo: refactor
        yolo_input_sg = {"img": img_masked_sg}
        yolo_output_sg = self.yolo_node.run(yolo_input_sg)
        output_counts_dict_sg = get_counts(yolo_output_sg)
        output_counts_dict['sg'] = output_counts_dict_sg

        # img_masked_jh
        # todo : refactor
        yolo_input_jh = {"img": img_masked_jh}
        yolo_output_jh = self.yolo_node.run(yolo_input_jh)
        output_counts_dict_jh = get_counts(yolo_output_jh)
        output_counts_dict['jh'] = output_counts_dict_jh

        return output_counts_dict

if __name__ == "__main__":
    img_path = "./data/View_from_Tuas_Checkpoint.jpg"
    inference_obj = inference()
    print (inference_obj.run_inference(img_path))


