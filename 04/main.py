def valid_p1(d):
    required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    return all(field in d for field in required_fields)

def valid_p2(d):
    def has_bounded_year(key, min, max):
        return key in d and d[key].isdigit() and len(d[key]) == 4 and min <= int(d[key]) <= max

    return (
        has_bounded_year("byr", 1920, 2002) and
        has_bounded_year("iyr", 2010, 2020) and
        has_bounded_year("eyr", 2020, 2030) and
        (hgt:=d.get("hgt",""))[:-2].isdigit() and
        (
            (hgt.endswith("cm") and 150 <= int(hgt[:-2]) <= 193) 
            or 
            (hgt.endswith("in") and 59 <= int(hgt[:-2]) <= 76)
        ) and
        (hcl:=d.get("hcl","")).startswith("#") and
        len(hcl) == 7 and
        all(c.isdigit() or c in "abcdef" for c in hcl[1:]) and
        d.get("ecl") in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"} and
        (pid:=d.get("pid","")).isdigit() and #allows hyphens but oh well
        len(pid) == 9
    )

def valid_p2(d):
    return (has_bounded_year := lambda key, min, max: key in d and d[key].isdigit() and len(d[key]) == 4 and min <= int(d[key]) <= max)("byr", 1920, 2002) and has_bounded_year("iyr", 2010, 2020) and has_bounded_year("eyr", 2020, 2030) and (hgt:=d.get("hgt",""))[:-2].isdigit() and ((hgt.endswith("cm") and 150 <= int(hgt[:-2]) <= 193) or (hgt.endswith("in") and 59 <= int(hgt[:-2]) <= 76)) and (hcl:=d.get("hcl","")).startswith("#") and len(hcl) == 7 and all(c.isdigit() or c in "abcdef" for c in hcl[1:]) and d.get("ecl") in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"} and (pid:=d.get("pid","")).isdigit() and len(pid) == 9
    

data = []
with open("input") as file:
    for entry in file.read().split("\n\n"):
        d = {}
        for item in entry.split():
            k,_,v = item.partition(":")
            d[k] = v
        data.append(d)

print(sum(1 for d in data if valid_p1(d)))
print(sum(1 for d in data if valid_p2(d)))
#145