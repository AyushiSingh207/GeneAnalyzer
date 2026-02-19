def parse_vcf(file_path):
    # Gene to RSID mapping - expanded with new variants
    gene_rsid_map = {
        'CYP2D6': ['rs1065852', 'rs113993960', 'rs3892097', 'rs5030655', 'rs16947', 'rs28371725', 'rs28371706', 'rs59421388'],
        'CYP2C19': ['rs4244285', 'rs4986893', 'rs12248560', 'rs28399504', 'rs12769205', 'rs17884712', 'rs56337013'],
        'CYP2C9': ['rs1799853', 'rs1057910', 'rs56109847', 'rs72558187', 'rs9332131'],
        'VKORC1': ['rs9923231', 'rs7294'],
        'SLCO1B1': ['rs4149056', 'rs2306283', 'rs11045819'],
        'TPMT': ['rs1142345', 'rs1800460', 'rs1800584', 'rs1800462'],
        'DPYD': ['rs3918290', 'rs55886062', 'rs1801265', 'rs67376798', 'rs1801159']
    }
    
    # Gene to star allele mapping - simplified
    gene_star_map = {
        'CYP2D6': {'0/1': '*1/*4', '1/1': '*4/*4'},
        'CYP2C19': {'0/1': '*1/*2', '1/1': '*2/*2'},
        'CYP2C9': {'0/1': '*1/*2', '1/1': '*2/*2'},
        'VKORC1': {'0/1': '-1639G/A', '1/1': '-1639A/A'}
    }

    parsed_data = {}
    
    try:
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith("#"):
                    continue

                columns = line.strip().split("\t")

                if len(columns) < 8:
                    continue

                rsid = columns[2]
                # Extract genotype from FORMAT field
                genotype = '0/0'
                if len(columns) > 9:
                    format_fields = columns[8].split(':')
                    sample_data = columns[9].split(':')
                    if 'GT' in format_fields:
                        gt_index = format_fields.index('GT')
                        if gt_index < len(sample_data):
                            genotype = sample_data[gt_index]
                
                # Find which gene this RSID belongs to
                for gene, rsids in gene_rsid_map.items():
                    if rsid in rsids:
                        # Determine star allele based on genotype
                        star = '*1/*1'  # default
                        if gene in gene_star_map:
                            # Check if it's heterozygous or homozygous
                            if genotype == '0/1' or genotype == '1/0':
                                star = gene_star_map[gene].get('0/1', '*1/*1')
                            elif genotype == '1/1':
                                star = gene_star_map[gene].get('1/1', '*1/*1')
                        
                        parsed_data[gene] = {
                            "star": star,
                            "rsid": rsid,
                            "genotype": genotype
                        }
                        print(f" Found {gene} with {rsid} - {star} (genotype: {genotype})")
                        
        return parsed_data
        
    except Exception as e:
        print(f" Error parsing VCF: {e}")
        return {}