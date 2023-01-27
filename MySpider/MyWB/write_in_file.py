import json
def write_in_file(output_datas,filename):
    if (not (output_datas is None)):
        with open(filename, 'a') as f:
            json.dump(output_datas, f)
            f.close()
    else:
        pass