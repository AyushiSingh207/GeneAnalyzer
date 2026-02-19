def parse_vcf(file_path):
    genes_of_interest = [
        "CYP2D6",
        "CYP2C19",
        "CYP2C9",
        "SLCO1B1",
        "TPMT",
        "DPYD"
    ]

    parsed_data = {}

    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("#"):
                continue

            columns = line.strip().split("\t")

            if len(columns) < 8:
                continue

            rsid = columns[2]
            info_field = columns[7]

            info_dict = {}
            for item in info_field.split(";"):
                if "=" in item:
                    key, value = item.split("=", 1)
                    info_dict[key] = value

            gene = info_dict.get("GENE")
            star = info_dict.get("STAR")

            if gene in genes_of_interest:
                parsed_data[gene] = {
                    "star": star,
                    "rsid": rsid
                }
    return parsed_data