from peekingduck.pipeline.nodes.model import yolo as pkd_yolo
import cv2
from collections import defaultdict

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
    missing_keys = [item for item in ["car", "motorcycle", "truck", "bus"] if item not in counts_dict.keys()]
    
    for key in missing_keys:
        counts_dict[key] = 0

    return dict(counts_dict)

class inference:

    def __init__(self):
        self.yolo_node = pkd_yolo.Node(model_type = "v4", detect= ["car", "motorcycle", "truck", "bus"], )
        
    def run_inference(self, img_path):
        image_orig = cv2.imread(img_path)
        image_orig = cv2.cvtColor(image_orig, cv2.COLOR_BGR2RGB)

        yolo_input = {"img": image_orig}
        yolo_output = self.yolo_node.run(yolo_input)
        output_counts_dict = get_counts(yolo_output)

        return output_counts_dict

if __name__ == "__main__":
    img_path = "./data/View_from_Tuas_Checkpoint.jpg"
    inference_obj = inference()
    print (inference_obj.run_inference(img_path))


