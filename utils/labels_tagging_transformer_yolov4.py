import os
import glob


def rindex(input_list, input_value):
    """get the last occurrence of a value in a list

    Args:
        input_list (list): 
        input_value (int):

    Returns:
        [int]: index of last occurrence
    """
    return len(input_list) - input_list[::-1].index(input_value) - 1

def tag_labels(raw_images_dir, tagged_labels_dir, tagged_dir):
    """[summary]

    Args:
        raw_images_dir (str): 
        tagged_labels_dir (str):
        tagged_dir (str):
    """
    output_file = raw_images_dir[:raw_images_dir.rindex("/")]+"/train.txt"
    file_label = open(f"{output_file}", "w")
    for frame in glob.glob(os.path.join(tagged_dir, '*')):
            frame_name = frame.split("/")[-1].split(".jpg")[0]
            
            
            filenames = []
            for classes in glob.glob(os.path.join(tagged_labels_dir, '*')):  
                    filenames.append(classes+"/"+frame_name.replace(".jpeg",".txt"))
            
            image_name = filenames[0].split("/")[-1].replace(".txt",".jpeg")
            label_str = ""
            for filename in filenames: 
                with open(filename) as infile:
                    for line in infile:
                        label_tag = line.split(" ")[0]
                        label_coordinates =[str(int(float(value)*1000000)) for value in line.split(" ")[1:]]
                        if filename == filenames[-1]:
                            label_str += f"{','.join(label_coordinates)},{label_tag}"
                        else:
                            label_str += f"{','.join(label_coordinates)},{label_tag} "

                    
            write_line = f"../.{raw_images_dir}/{image_name} {label_str}"
            #../../data/artifacts/images/frame2.jpg 492405,440201,398003,613426,0 439019,581019,167969,334877,1
            file_label.write(write_line)
            file_label.write("\n")
    file_label.close()

if __name__ == "__main__":
    tag_labels(raw_images_dir = "./data/shopfront/images", tagged_labels_dir = "./data/shopfront/shopfront_labels", tagged_dir = "./data/shopfront/shopfront_tagging/0")