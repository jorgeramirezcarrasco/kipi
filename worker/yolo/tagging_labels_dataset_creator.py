import os
import glob


labels_dir = "../../data/artifacts/labels"
tagged_labels_dir = "../../data/artifacts/newlabels"
tagged_dir = "../../data/artifacts/tagging/0"
for frame in glob.glob(os.path.join(tagged_dir, '*')):
        frame_name = frame.split("/")[-1].split(".jpg")[0]
        file_label = open(f"../../data/artifacts/labels/{frame_name}.txt", "w")
        filenames = []
        for classes in glob.glob(os.path.join(tagged_labels_dir, '*')):  
                filenames.append(classes+"/"+frame_name+".txt")        
        for filename in filenames:
                with open(filename) as infile:
                        for line in infile:
                                file_label.write(line)
                                file_label.write("\n")
        file_label.close()
