from src.pull_data import get_data, get_data_direct
from src.util import open_yaml_file
from src.inference import inference
import pandas as pd
from datetime import date, datetime

def main(cfg_path="config/config.yml", from_path = False):

    cfg_obj = open_yaml_file(fname = cfg_path)
    
    counts_df = pd.read_csv("./data/counts_dataset.csv")
    curr_date = date.today()
    curr_time = datetime.now()
    curr_time = curr_time.strftime("%H:%M:%S")

    #initiate inference object
    inference_obj = inference()

    # with the files, do object detection and get the counts of objects for each image type
    if from_path:
        # download the images and get list of the image file names
        img_fnames = get_data(cfg_obj)
        for fname in img_fnames:
            img_path = f"./data/{fname}"
            counts_of_object = inference_obj.run_inference(img_path)

            new_row = pd.Series({'date': curr_date,
                                'time': curr_time, 
                                'view': fname[:-3],
                                'car': counts_of_object['car'],
                                'motorcycle': counts_of_object['motorcycle'] + counts_of_object['motorbike'],
                                'large_vehicle': counts_of_object['bus'] + counts_of_object['truck']})

            counts_df = pd.concat([counts_df, new_row.to_frame().T], ignore_index=True)

        # TODO - remove files after running inference
    
    else: 
        # alternative is to iterate and get image directly to run inference and save into csv
        img_dict = get_data_direct(cfg_obj)
        for text, img_data in img_dict.items():
            counts_of_object = inference_obj.run_inference_direct(img_data, text)

            # todo: output dictionary {sg: {car: , ...}, jh: {...}}
            for key in counts_of_object.keys():
            # new_row = pd.Series ... counts_of_object[key]['car']
                # new_row = pd.Series({'date': curr_date,
                #                     'time': curr_time, 
                #                     'view': text,
                #                     'car': counts_of_object['car'],
                #                     'motorcycle': counts_of_object['motorcycle'],
                #                     'large_vehicle': counts_of_object['bus'] + counts_of_object['truck']})
                new_row = pd.Series({'date': curr_date,
                                    'time': curr_time, 
                                    'view': f"{text}_to_{key}",
                                    'car': counts_of_object[key]['car'],
                                    'motorcycle': counts_of_object['motorcycle'] + counts_of_object['motorbike'],
                                    'large_vehicle': counts_of_object[key]['bus'] + counts_of_object[key]['truck']})

                counts_df = pd.concat([counts_df, new_row.to_frame().T], ignore_index=True)
    
    counts_df.to_csv("./data/counts_dataset.csv", index = False)

    return

if __name__ == "__main__":
    main()