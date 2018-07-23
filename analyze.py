import glob
import json
import sys
import csv


def get_json_files():
    name = "*.json"
    if len(sys.argv) > 1:
        name = "/".join([sys.argv[1], name])
    print("Getting files from %s" % name)
    return glob.glob(name)


def unique_links(obj):
    links = []

    for i in reversed(range(len(obj))):
        l = obj[i]['url']
        if l in links:
            obj.pop(i)
        else:
            links.append(l)

    return obj

def remove_dupe(obj):
    hashes = []

    for i in reversed(range(len(obj))):
        h = hash(frozenset(obj[i].items()))
        if h in hashes:
            obj.pop(i)
        else:
            hashes.append(h)

    return obj


def unique_websites(obj):
    websites = []

    for i in reversed(range(len(obj))):
        url = obj[i]["url"].split("/")[2]
        if url not in websites:
            websites.append(url)

    return websites


def get_unique_websites(obj, w):
    for i in reversed(range(len(w))):
        if w[i] in obj:
            w.pop(i)

    return w


def add_src(obj, src):
    for o in obj:
        o['src'] = src
    return obj


def finalize(group, growth=True):
    print("-")
    groups = {}
    hosts = []
    links = []
    unique = []
    growth_d = []
    for k, v in sorted(group.items()):
        print("Count for %s: %i" % (k, len(v)))
        _v = remove_dupe(v)
        hosts.extend(_v)
        print("Unique signatures for %s: %i" % (k, len(_v)))
        _l = add_src(unique_links(_v), k)
        links.extend(_l)
        print("Unique URLs for %s: %i" % (k, len(_l)))
        _w = unique_websites(_l)
        unique.extend(_w)
        print("Unique websites for %s: %i" % (k, len(_w)))
        if growth:
            g = k.split('.')[0]
            if g not in groups.keys():
                groups[g] = []
            _u = get_unique_websites(groups[g], _w)
            print("Growth of unique websites for %s: %i" % (k, len(_u)))
            growth_d.append({
                "growth": len(_u),
                "val": k
            })
            groups[g].extend(_u)
        print("-")
    if growth:
        print("Total")  # for sanity check
        for item in groups.items():
            print("length of %s: %i" % (item[0], len(item[1])))

    unique = set(unique)

    return hosts, unique, links, growth_d


def agg_all():
    jsonFiles = get_json_files()
    group = {
        "awstats": [],
        "wpCont": [],
        "wpTag": [],
        "postnuke": []
    }
    for jf in jsonFiles:
        fileName = jf.split('/')[-1]
        if fileName.startswith("awstats-data-file") or \
           fileName.startswith("duckduckgo") or \
           fileName.startswith("bing") or \
           fileName.startswith("dogpile"):
            with open(jf, "r") as f:
                group["awstats"].extend(json.load(f))
        elif fileName.startswith("wordpress-contributors"):
            with open(jf, "r") as f:
                group["wpCont"].extend(json.load(f))
        elif fileName.startswith("wordpress-tags"):
            with open(jf, "r") as f:
                group["wpTag"].extend(json.load(f))
        elif fileName.startswith("postnuke"):
            with open(jf, "r") as f:
                group["postnuke"].extend(json.load(f))
    return finalize(group, growth=False)


def agg_hour():
    jsonFiles = get_json_files()
    group = {}
    for jf in jsonFiles:
        fileName = jf.split('/')[-1]
        if fileName.startswith("awstats-data-file") or \
           fileName.startswith("duckduckgo") or \
           fileName.startswith("bing") or \
           fileName.startswith("dogpile"):
            with open(jf, "r") as f:
                n = "".join(fileName.split(".")[-3:-1])
                n = "".join(["awstats", n])
                group[n] = json.load(f)
        elif fileName.startswith("wordpress-contributors"):
            with open(jf, "r") as f:
                n = "".join(fileName.split(".")[-3:-1])
                n = "".join(["wpCont", n])
                group[n] = json.load(f)
        elif fileName.startswith("wordpress-tags"):
            with open(jf, "r") as f:
                n = "".join(fileName.split(".")[-3:-1])
                n = "".join(["wpTag", n])
                group[n] = json.load(f)
        elif fileName.startswith("postnuke"):
            with open(jf, "r") as f:
                n = "".join(fileName.split(".")[-3:-1])
                n = "".join(["postnuke", n])
                group[n] = json.load(f)
    return finalize(group)


def agg_day():
    jsonFiles = get_json_files()
    group = {}
    for jf in jsonFiles:
        fileName = jf.split('/')[-1]
        if fileName.startswith("awstats-data-file") or \
           fileName.startswith("duckduckgo") or \
           fileName.startswith("bing") or \
           fileName.startswith("dogpile"):
            with open(jf, "r") as f:
                n = "".join(fileName.split(".")[-3:-1]).split("T")[0]
                n = ".".join(["awstats", n])
                if n not in group.keys():
                    group[n] = json.load(f)
                else:
                    group[n].extend(json.load(f))
        elif fileName.startswith("wordpress-contributors"):
            with open(jf, "r") as f:
                n = "".join(fileName.split(".")[-3:-1]).split("T")[0]
                n = ".".join(["wpCont", n])
                if n not in group.keys():
                    group[n] = json.load(f)
                else:
                    group[n].extend(json.load(f))
        elif fileName.startswith("wordpress-tags"):
            with open(jf, "r") as f:
                n = "".join(fileName.split(".")[-3:-1]).split("T")[0]
                n = ".".join(["wpTag", n])
                if n not in group.keys():
                    group[n] = json.load(f)
                else:
                    group[n].extend(json.load(f))
        elif fileName.startswith("postnuke"):
            with open(jf, "r") as f:
                n = "".join(fileName.split(".")[-3:-1]).split("T")[0]
                n = ".".join(["postnuke", n])
                if n not in group.keys():
                    group[n] = json.load(f)
                else:
                    group[n].extend(json.load(f))
    return finalize(group)


def data_to_csv(data, name, json=False):
    csvwriter = csv.writer(open(name, "w+"))

    if json:
        count = 0
        for d in data:
            if count == 0:
                    header = d.keys()
                    csvwriter.writerow(header)
            csvwriter.writerow(d.values())
            count += 1
    else:
        csvwriter.writerow(data)
        count = len(data)

    print("Written %d data to %s" % (count, name))


if __name__ == "__main__":
    print("Daily stats:")
    _, _, _, growth = agg_day()
    print("--------------------------------")
    print("All stats:")
    hosts, unique, links, _ = agg_all()
    print("--------------------------------")
    data_to_csv(hosts, "signatures_list.csv", json=True)
    data_to_csv(links, "url_list.csv", json=True)
    data_to_csv(growth, "growth_list.csv", json=True)
    data_to_csv(unique, "host_list.csv")
