import re
import argparse
import json


def write(text, file=None):
    if file is not None:
        file.write(str(text))
    print(text)


def line_to_dict(line, include_raw=False):
    line_list = line.split(" ")
    line_dict = {"ip": line_list[0],
                 "date": re.findall(r"\[(.*?)\]", line)[0],
                 "method": line_list[5][1:],
                 "url": line_list[6],
                 "status": int(line_list[8]),
                 "bytes_sent": 0 if (bs := line_list[9]) == "-" else int(bs)
                 }
    if include_raw:
        line_dict["raw"] = line
    return line_dict


def group_by(data, field, print_status=False):
    unique_data = set([rec[field] for rec in data])
    if print_status:
        print(f"grouping by {field}")
        print(f"found {len(unique_data)} unique units")
        print(f"proccessing...")
    res = []
    for i, unique_val in enumerate(unique_data):
        if print_status:
            l = len(unique_data)
            if l > 10 and i % int(l/10) == 0:
                print(f"{int(i*100/len(unique_data))}% done")
        res.append([rec for rec in data if rec[field] == unique_val])
    print("done")
    return res


def process(data, file=None):
    res_j = {}

    #Общее количество запросов
    req_count = {"ALL": len(
        [req for req in data if req["status"] is not None])}
    write("\n Запросов всего:\n", file)
    write(req_count, file)
    res_j["Count total"] = req_count

    #Количество запросов по типу
    #все используемые методы
    methods = set([req["method"] for req in data if len(req["method"]) < 10])
    for method in methods:
        req_count[method] = len(
            [req for req in data if req["method"] == method])

    write("\n Запросов по методу:\n", file)
    write(req_count, file)
    res_j["count_by_method"] = req_count

    #Топ 10 самых больших по размеру запросов, должно быть видно url, код, число запросов
    biggest = sorted(data, key=lambda i: i["bytes_sent"], reverse=True)[:10]
    write("\n Топ 10 самых больших по размеру запросов:\n", file)
    write("\n".join(list(map(str, biggest))), file)
    res_j["top_biggest_total"] = biggest

    # Топ 10 запросов по количеству, которые завершились
    # клиентской ошибкой

    # все клиентские ошибки
    errors400 = [req for req in data if req["status"]//100 == 4]
    errors400 = sorted(
        group_by(errors400, "url", True), key=lambda i: len(i), reverse=True)[:10]
    errors400 = [{"url": rec[0]["url"], "count":len(
        rec)} for rec in errors400]
    write("\n Топ 10 клиентских ошибок по количеству запросов(для url):\n", file)
    write("\n".join(list(map(str, errors400))), file)
    res_j["top_client_err_by_count"] = errors400

    #Топ 10 запросов серверных ошибок по размеру запроса,
    # должно быть видно url, статус код, ip адрес
    errors500 = [req for req in data if req["status"]//100 == 5]
    errors500 = sorted(
        errors500, key=lambda i: i["bytes_sent"], reverse=True)[:10]
    write("\n Топ 10 серверных ошибок по размеру запроса:\n", file)
    write("\n".join(list(map(str, errors500))), file)
    res_j["top_server_err_by_count"] = errors500
    return res_j

parser = argparse.ArgumentParser(description='Logs analyse')
parser.add_argument('-f', action="store",
                    dest="filename", default="access.log")
parser.add_argument('-d', action="store", dest="file_dst", default="out.txt")
parser.add_argument('-j', action="store", dest="json", default=False, type=bool)

args = parser.parse_args()

data = []
with open(args.filename) as f:
    data = f.readlines()
data = list(map(line_to_dict, data))


with open(args.file_dst, "w") as f:
    if args.json is not None and args.json is True:
        obj = process(data, file=f)
        with open(args.file_dst+".json","w") as json_f:
            json_f.write(json.dumps(obj))
    else:
        process(data, file=f)
