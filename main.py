import glob
import os
import string
import cairosvg

class Person:
    def __init__(self, nama, job, emailaddres, telp, no_serti):
        self.nama = nama
        self.job = job
        self.emailaddres = emailaddres
        self.telp = telp
        self.no_serti = no_serti

def get_names_as_list():

    # Get file for names
    text_file = glob.glob('*.txt')
    # wild card to catch all the files ending with txt and return as list of files

    if len(text_file) != 1:
        raise ValueError('should be only one txt file in the current directory')

    # Open file
    input_file = open(text_file[0], "r")

    # read file
    try_read = input_file.read()

    # put file contents as string list split by line
    temp_list = try_read.splitlines()

    # close file
    input_file.close()

    # find and remove duplicate
    temp_list = list(dict.fromkeys(temp_list))

    return temp_list

def get_source_svg():
    source_svg_list = glob.glob("*.svg")

    if len(source_svg_list) != 1:
        raise ValueError('should be only one svg file in the current directory')

    input_file = open(source_svg_list[0], "r")
    buffer_str = input_file.read()
    input_file.close()
    return buffer_str

def generate_svg(buffer_str, person_class_list):
    
    percentage = 0
    for person in person_class_list:
        print("Generating svg for:", person.nama, "sebagai", person.job, "dengan email:", person.emailaddres)

        temp_string = buffer_str
        temp_string = temp_string.replace("{{role}}", person.job)
        temp_string = temp_string.replace("{{nama_peserta}}", person.nama)
        temp_string = temp_string.replace("{{no_serti}}", person.no_serti)
        output_file = open("out/{} - {}.svg".format(person.nama, person.job), "w")
        output_file.write(temp_string)
        output_file.close()
        percentage += 1
        print("Done : {}/{} ({:.2f}%)".format(percentage, len(person_class_list), (percentage/len(person_class_list))*100))

def generate_pdf():
    # List files in output folder then put them in list
    svg_file_list = glob.glob("out/*.svg")

    # # find and remove duplicate, unlikely but just incase
    # svg_file_list = list(dict.fromkeys(svg_file_list))

    percentage = 0
    for person_name in svg_file_list:
        # deleting filepath & extension so only filename remain
        person_name = person_name.replace(".svg","")
        person_name = person_name.replace("out\\","")
        # path_output = "out/{}.pdf"
        # path_input = "out/{}.svg"

        # Converting to pdf
        print("Generating pdf for:", person_name, "...")
        # cairosvg.svg2pdf(file_obj=open(path_input.format(person_name), "rb"), dpi = 300, write_to=path_output.format(person_name))
        os.system(f'inkscape "--export-area-page" "out\{person_name}.svg" --export-type=pdf')
        percentage += 1
        print("Done : {}/{} ({:.2f}%)".format(percentage, len(svg_file_list), (percentage/len(svg_file_list))*100))

def main():

    temp_list = get_names_as_list()

    # Categorize name list as person class w/ name, job, and email address attributes
    person_class_list = []
    i = 0
    while i < len(temp_list):
        # seperate list
        temp_list[i] = temp_list[i].split(";")
        # put into class
        person_class_list.append(Person(temp_list[i][0], temp_list[i][1], temp_list[i][2], temp_list[i][3], temp_list[i][4]))
        i += 1

    # Creating output folder
    # folder_list = ["Peserta", "Pemakalah", "Panitia", "Moderator", "MC", "Pemakalah sbg Peserta"]
    if os.path.exists("out/"):
        print("Output folder \"out\" already exists...")
        pass
    else:
        print("Output folder \"out\" doesn't exist. Creating one...")
        # for folder_name in folder_list:
            # os.makedirs("out/{}".format(folder_name))
        os.mkdir("out/")

    # Read svg file as string then put in buffer
    buffer_str = get_source_svg()

    # Generating svg files
    generate_svg(buffer_str, person_class_list)

    # Generating pdf files
    generate_pdf()

if __name__ == "__main__":
    main()
