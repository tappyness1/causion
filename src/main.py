from src.pull_data import get_data
from src.util import open_yaml_file
from src.inference import inference
import pandas as pd
from datetime import date, datetime

def main(cfg_path="config/config.yml"):

    cfg_obj = open_yaml_file(fname = cfg_path)

    # download the images and get list of the image file names
    img_fnames = get_data(cfg_obj)

    counts_df = pd.read_csv("./data/counts_dataset.csv")
    curr_date = date.today()
    curr_time = datetime.now()
    curr_time = curr_time.strftime("%H:%M:%S")

    # with the files, do object detection and get the counts of objects for each image type
    inference_obj = inference()
    for fname in img_fnames:
        img_path = f"./data/{fname}"
        counts_of_object = inference_obj.run_inference(img_path)

        new_row = pd.Series({'date': curr_date,
                             'time': curr_time, 
                             'view': fname[:-3],
                             'car': counts_of_object['car'],
                             'motorcycle': counts_of_object['motorcycle'],
                             'large_vehicle': counts_of_object['bus'] + counts_of_object['truck']})

        counts_df = pd.concat([counts_df, new_row.to_frame().T], ignore_index=True)
    
    counts_df.to_csv("./data/counts_dataset.csv", index = False)

    # TODO - remove files after running inference

    return

if __name__ == "__main__":
    main()