import os
import pandas as pd

from kgcnn.data.crystal import CrystalDataset
from kgcnn.data.download import DownloadDataset
from kgcnn.data.utils import load_json_file, save_json_file


class MatBenchDataset2020(CrystalDataset, DownloadDataset):
    r"""Base class for loading graph datasets from `MatBench <https://matbench.materialsproject.org/>`__ , collection
    of materials datasets. For graph learning only those with structure are relevant.
    Process and loads from serialized :obj:`pymatgen` structures.

    .. note::

        This class does not follow the interface of `MatBench <https://github.com/materialsproject/matbench>`__
        and therefore also not the original splits required for submission of benchmark values.

    Matbench is an automated leaderboard for benchmarking state of the art ML algorithms predicting a diverse range
    of solid materials' properties. It is hosted and maintained by the
    `Materials Project <https://materialsproject.org/>`_ .

    `Matbench <https://www.nature.com/articles/s41524-020-00406-3>`__ is an `ImageNet <https://image-net.org/>`__
    for materials science; a curated set of 13 supervised, pre-cleaned, ready-to-use ML tasks for benchmarking
    and fair comparison.
    The tasks span a wide domain of inorganic materials science applications including electronic, thermodynamic,
    mechanical, and thermal properties among crystals, 2D materials, disordered metals, and more.

    References:

        (1) Dunn, A., Wang, Q., Ganose, A. et al. Benchmarking materials property prediction methods: the Matbench
            test set and Automatminer reference algorithm. npj Comput Mater 6, 138 (2020).
            `<https://doi.org/10.1038/s41524-020-00406-3>`_ .
    
    """

    datasets_download_info = {
        "matbench_steels": {"dataset_name": "matbench_steels",
                            "download_file_name": 'matbench_steels.json.gz',
                            "data_directory_name": "matbench_steels", 
                            "extract_gz": True,
                            "extract_file_name": 'matbench_steels.json'},
        "matbench_jdft2d": {"dataset_name": "matbench_jdft2d",
                            "download_file_name": 'matbench_jdft2d.json.gz',
                            "data_directory_name": "matbench_jdft2d", 
                            "extract_gz": True,
                            "extract_file_name": 'matbench_jdft2d.json'},
        "matbench_phonons": {"dataset_name": "matbench_phonons",
                             "download_file_name": 'matbench_phonons.json.gz',
                             "data_directory_name": "matbench_phonons", "extract_gz": True,
                             "extract_file_name": 'matbench_phonons.json'},
        "matbench_expt_gap": {"dataset_name": "matbench_expt_gap",
                              "download_file_name": 'matbench_expt_gap.json.gz',
                              "data_directory_name": "matbench_expt_gap", "extract_gz": True,
                              "extract_file_name": 'matbench_expt_gap.json'},
        "matbench_dielectric": {"dataset_name": "matbench_dielectric",
                                "download_file_name": 'matbench_dielectric.json.gz',
                                "data_directory_name": "matbench_dielectric", "extract_gz": True,
                                "extract_file_name": 'matbench_dielectric.json'},
        "matbench_expt_is_metal": {"dataset_name": "matbench_expt_is_metal",
                                   "download_file_name": 'matbench_expt_is_metal.json.gz',
                                   "data_directory_name": "matbench_expt_is_metal", "extract_gz": True,
                                   "extract_file_name": 'matbench_expt_is_metal.json'},
        "matbench_glass": {"dataset_name": "matbench_glass",
                           "download_file_name": 'matbench_glass.json.gz',
                           "data_directory_name": "matbench_glass", "extract_gz": True,
                           "extract_file_name": 'matbench_glass.json'},
        "matbench_log_gvrh": {"dataset_name": "matbench_log_gvrh",
                              "download_file_name": 'matbench_log_gvrh.json.gz',
                              "data_directory_name": "matbench_log_gvrh", "extract_gz": True,
                              "extract_file_name": 'matbench_log_gvrh.json'},
        "matbench_log_kvrh": {"dataset_name": "matbench_log_kvrh",
                              "download_file_name": 'matbench_log_kvrh.json.gz',
                              "data_directory_name": "matbench_log_kvrh", "extract_gz": True,
                              "extract_file_name": 'matbench_log_kvrh.json'},
        "matbench_perovskites": {"dataset_name": "matbench_perovskites",
                                 "download_file_name": 'matbench_perovskites.json.gz',
                                 "data_directory_name": "matbench_perovskites", "extract_gz": True,
                                 "extract_file_name": 'matbench_perovskites.json'},

        "matbench_mp_gap": {"dataset_name": "matbench_mp_gap",
                            "download_file_name": 'matbench_mp_gap.json.gz',
                            "data_directory_name": "matbench_mp_gap", "extract_gz": True,
                            "extract_file_name": 'matbench_mp_gap.json'},


        "matbench_mp_is_metal": {"dataset_name": "matbench_mp_is_metal",
                                 "download_file_name": 'matbench_mp_is_metal.json.gz',
                                 "data_directory_name": "matbench_mp_is_metal", "extract_gz": True,
                                 "extract_file_name": 'matbench_mp_is_metal.json'},
        "matbench_mp_e_form": {"dataset_name": "matbench_mp_e_form",
                               "download_file_name": 'matbench_mp_e_form.json.gz',
                               "data_directory_name": "matbench_mp_e_form", "extract_gz": True,
                               "extract_file_name": 'matbench_mp_e_form.json'},

         "mp_LFP_gap": {"dataset_name": "mp_LFP_gap",
                            "download_file_name": 'mp_LFP_gap.json.gz',
                            "data_directory_name": "mp_LFP_gap", "extract_gz": True,
                            "extract_file_name": 'mp_LFP_gap.json'},

        "band_gap_order_exp": {"dataset_name": "band_gap_order_exp",
                            "download_file_name": 'band_gap_order_exp.json.gz',
                            "data_directory_name": "band_gap_order_exp", "extract_gz": True,
                            "extract_file_name": 'band_gap_order_exp.json'},  


        "multifidelity_band_gap": {"dataset_name": None,
                               "download_file_name": "multifidelity_band_gap.json",
                               "data_directory_name": "multifidelity_band_gap", "extract_gz": False,
                               "extract_file_name": None},       

        "include_li_mp_band_gap": {"dataset_name": None,
                               "download_file_name": "include_li_mp_band_gap.json",
                               "data_directory_name": "include_li_mp_band_gap", "extract_gz": False,
                               "extract_file_name": None},     


        "sample_all_materials_data_form_processed": {"dataset_name": None,
                               "download_file_name": "sample_all_materials_data_form_processed.json",
                               "data_directory_name": "sample_all_materials_data_form_processed", "extract_gz": False,
                               "extract_file_name": None},   

        "ml_e_form_exp": {"dataset_name": None,
                               "download_file_name": "ml_e_form_exp.json",
                               "data_directory_name": "ml_e_form_exp", "extract_gz": False,
                               "extract_file_name": None},   
        
        "sample_all_materials_data_ehull_processed": {"dataset_name": None,
                               "download_file_name": "sample_all_materials_data_ehull_processed.json",
                               "data_directory_name": "sample_all_materials_data_ehull_processed", "extract_gz": False,
                               "extract_file_name": None},   
        
        "include_li_mp_eform": {"dataset_name": None,
                               "download_file_name": "include_li_mp_eform.json",
                               "data_directory_name": "include_li_mp_eform", "extract_gz": False,
                               "extract_file_name": None},   
        
        "sample_all_materials_data_form_processed_include_li_more_than_neg2": {"dataset_name": None,
                               "download_file_name": "sample_all_materials_data_form_processed_include_li_more_than_neg2.json",
                               "data_directory_name": "sample_all_materials_data_form_processed_include_li_more_than_neg2", "extract_gz": False,
                               "extract_file_name": None},   
        
        "li_sse_eform_mp_datasest": {"dataset_name": None,
                               "download_file_name": "li_sse_eform_mp_datasest.json",
                               "data_directory_name": "li_sse_eform_mp_datasest", "extract_gz": False,
                               "extract_file_name": None},  
        "include_li_mp_ehull": {"dataset_name": None,
                               "download_file_name": "include_li_mp_ehull.json",
                               "data_directory_name": "include_li_mp_ehull", "extract_gz": False,
                               "extract_file_name": None}, 
        
        "li_sse_ehull_mp_datasest": {"dataset_name": None,
                               "download_file_name": "li_sse_ehull_mp_datasest.json",
                               "data_directory_name": "li_sse_ehull_mp_datasest", "extract_gz": False,
                               "extract_file_name": None}, 
        
        "all_materials_gvrh_data_processed": {"dataset_name": None,
                               "download_file_name": "all_materials_gvrh_data_processed.json",
                               "data_directory_name": "all_materials_gvrh_data_processed", "extract_gz": False,
                               "extract_file_name": None}, 

        "include_li_mp_gvrh": {"dataset_name": None,
                               "download_file_name": "include_li_mp_gvrh.json",
                               "data_directory_name": "include_li_mp_gvrh", "extract_gz": False,
                               "extract_file_name": None}, 

        "li_sse_shear_modulus_mp_datasest": {"dataset_name": None,
                               "download_file_name": "li_sse_shear_modulus_mp_datasest.json",
                               "data_directory_name": "li_sse_shear_modulus_mp_datasest", "extract_gz": False,
                               "extract_file_name": None}, 
        
        "all_materials_kvrh_data_processed": {"dataset_name": None,
                               "download_file_name": "all_materials_kvrh_data_processed.json",
                               "data_directory_name": "all_materials_kvrh_data_processed", "extract_gz": False,
                               "extract_file_name": None}, 
        "include_li_mp_kvrh": {"dataset_name": None,
                               "download_file_name": "include_li_mp_kvrh.json",
                               "data_directory_name": "include_li_mp_kvrh", "extract_gz": False,
                               "extract_file_name": None}, 
        "li_sse_bulk_modulus_mp_datasest": {"dataset_name": None,
                               "download_file_name": "li_sse_bulk_modulus_mp_datasest.json",
                               "data_directory_name": "li_sse_bulk_modulus_mp_datasest", "extract_gz": False,
                               "extract_file_name": None}, 
        "li_sse_gap_mp_datasest": {"dataset_name": None,
                               "download_file_name": "li_sse_gap_mp_datasest.json",
                               "data_directory_name": "li_sse_gap_mp_datasest", "extract_gz": False,
                               "extract_file_name": None}, 

        "sulfides_band_mp_dataset": {"dataset_name": None,
                               "download_file_name": "sulfides_band_mp_dataset.json",
                               "data_directory_name": "sulfides_band_mp_dataset", "extract_gz": False,
                               "extract_file_name": None}, 


  
    }
    datasets_prepare_data_info = {
        "matbench_steels": {"file_column_name": "composition"},
        "matbench_jdft2d": {"file_column_name": "structure"},
        "matbench_phonons": {"file_column_name": "structure"},
        "matbench_expt_gap": {"file_column_name": "composition"},
        "matbench_dielectric": {"file_column_name": "structure"},
        "matbench_expt_is_metal": {"file_column_name": "composition"},
        "matbench_glass": {"file_column_name": "composition"},
        "matbench_log_gvrh": {"file_column_name": "structure"},
        "matbench_log_kvrh": {"file_column_name": "structure"},
        "matbench_perovskites": {"file_column_name": "structure"},
        "matbench_mp_gap": {"file_column_name": "structure"},
        "matbench_mp_is_metal": {"file_column_name": "structure"},
        "matbench_mp_e_form": {"file_column_name": "structure"},

        "mp_LFP_gap": {"file_column_name": "structure"},
        "band_gap_order_exp": {"file_column_name": "structure"},
        "multifidelity_band_gap": {"file_column_name": "structure"},

        "include_li_mp_band_gap": {"file_column_name": "structure"},
         "li_sse_gap_mp_datasest": {"file_column_name": "structure"},
        "sample_all_materials_data_form_processed": {"file_column_name": "structure"},
        "ml_e_form_exp": {"file_column_name": "structure"},
        "sample_all_materials_data_ehull_processed": {"file_column_name": "structure"},
        "include_li_mp_eform": {"file_column_name": "structure"},

        "sample_all_materials_data_form_processed_include_li_more_than_neg2": {"file_column_name": "structure"},
        "li_sse_eform_mp_datasest": {"file_column_name": "structure"},
        "include_li_mp_ehull": {"file_column_name": "structure"},

        "li_sse_ehull_mp_datasest": {"file_column_name": "structure"},
        "all_materials_gvrh_data_processed": {"file_column_name": "structure"},

        "include_li_mp_gvrh": {"file_column_name": "structure"},
        "li_sse_shear_modulus_mp_datasest": {"file_column_name": "structure"},
        "all_materials_kvrh_data_processed": {"file_column_name": "structure"},

        "include_li_mp_kvrh": {"file_column_name": "structure"},
        "li_sse_bulk_modulus_mp_datasest": {"file_column_name": "structure"},

        "sulfides_band_mp_dataset": {"file_column_name": "structure"},

    }


    datasets_read_in_memory_info = {
        "matbench_steels": {"label_column_name": "yield strength"},
        "matbench_jdft2d": {"label_column_name": "exfoliation_en"},
        "matbench_phonons": {"label_column_name": "last phdos peak"},
        "matbench_expt_gap": {"label_column_name": "gap expt"},
        "matbench_dielectric": {"label_column_name": "n"},
        "matbench_expt_is_metal": {"label_column_name": "is_metal"},
        "matbench_glass": {"label_column_name": "gfa"},
        "matbench_log_gvrh": {"label_column_name": "log10(G_VRH)"},
        "matbench_log_kvrh": {"label_column_name": "log10(K_VRH)"},
        "matbench_perovskites": {"label_column_name": "e_form"},
        "matbench_mp_gap": {"label_column_name": "gap pbe"},
        "matbench_mp_is_metal": {"label_column_name": "is_metal"},
        "matbench_mp_e_form": {"label_column_name": "e_form"},

        "mp_LFP_gap": {"label_column_name": "gap"},
        "band_gap_order_exp": {"label_column_name": "band_gap"},
        "multifidelity_band_gap": {"label_column_name": "multifidelity_band_gap", "label_column_name_s": "index"},
        "include_li_mp_band_gap": {"label_column_name": "include_li_band_gap", "label_column_name_s": "index"},
        "li_sse_gap_mp_datasest": {"label_column_name": "li_sse_band_gap", "label_column_name_s": "index"},
        "sample_all_materials_data_form_processed": {"label_column_name": "formation_energy_per_atom", "label_column_name_s": "index"},
        "ml_e_form_exp": {"label_column_name": "formation_energy_per_atom", "label_column_name_s": "index"},
        "sample_all_materials_data_ehull_processed": {"label_column_name": "energy_above_hull", "label_column_name_s": "index"},
        "include_li_mp_eform": {"label_column_name": "formation_energy_per_atom", "label_column_name_s": "index"},

        "sample_all_materials_data_form_processed_include_li_more_than_neg2": {"label_column_name": "formation_energy_per_atom", "label_column_name_s": "index"},

        "li_sse_eform_mp_datasest": {"label_column_name": "formation_energy_per_atom", "label_column_name_s": "index"},
    
        "include_li_mp_ehull": {"label_column_name": "energy_above_hull", "label_column_name_s": "index"},

        "li_sse_ehull_mp_datasest": {"label_column_name": "e_above_hull", "label_column_name_s": "index"},
        "all_materials_gvrh_data_processed": {"label_column_name": "shear_modulus_vrh", "label_column_name_s": "index"},

        "include_li_mp_gvrh": {"label_column_name": "shear_modulus_vrh", "label_column_name_s": "index"},

        "li_sse_shear_modulus_mp_datasest": {"label_column_name": "shear_modulus_vrh", "label_column_name_s": "index"},
        "all_materials_kvrh_data_processed": {"label_column_name": "bulk_modulus_vrh", "label_column_name_s": "index"},

        "include_li_mp_kvrh": {"label_column_name": "bulk_modulus_vrh", "label_column_name_s": "index"},

        "li_sse_bulk_modulus_mp_datasest": {"label_column_name": "bulk_modulus_vrh", "label_column_name_s": "index"},

        "sulfides_band_mp_dataset": {"label_column_name": "band gap", "label_column_name_s": "index"},

    
    }

    def __init__(self, dataset_name: str, reload: bool = False, verbose: int = 10):
        """Initialize a `GraphTUDataset` instance from string identifier.

        Args:
            dataset_name (str): Name of a dataset.
            reload (bool): Download the dataset again and prepare data on disk.
            verbose (int): Print progress or info for processing where 60=silent. Default is 10.
        """
        if not isinstance(dataset_name, str):
            raise ValueError("Please provide string identifier for TUDataset.")

        CrystalDataset.__init__(self, verbose=verbose, dataset_name=dataset_name)

        # Prepare download
        if dataset_name in self.datasets_download_info:
            self.download_info = self.datasets_download_info[dataset_name]
            self.download_info.update({"download_url": "https://ml.materialsproject.org/projects/" +
                                                       self.download_info["download_file_name"]})
        else:
            raise ValueError(
                "Can not resolve %s as a MatBench dataset. Pick " % dataset_name, self.datasets_download_info.keys(),
                "For new dataset, add to `datasets_download_info` list manually.")

        DownloadDataset.__init__(self, **self.download_info, reload=reload, verbose=verbose)

        self.data_directory = os.path.join(self.data_main_dir, self.data_directory_name) # "./matbench_dielectric"
        file_name_download = self.download_file_name if self.extract_file_name is None else self.extract_file_name # 'matbench_steels.json'
        self.file_name = "%s.csv" % os.path.splitext(file_name_download)[0]  # 'matbench_dielectric.json'  matbench_dielectric.csv
        self.dataset_name = dataset_name  # "matbench_dielectric"
        self.require_prepare_data = True 
        self.fits_in_memory = True

        if self.require_prepare_data:
            self.prepare_data(overwrite=reload, **self.datasets_prepare_data_info[self.dataset_name]) #{"file_column_name": "structure"}
        if self.fits_in_memory:
            self.read_in_memory(**self.datasets_read_in_memory_info[self.dataset_name]) # {"label_column_name": "n"}
            # Read structures from pymatgen json serialization and convert them into graph information


    def prepare_data(self, file_column_name: str = None, overwrite: bool = False):

        file_name_download = self.download_file_name if self.extract_file_name is None else self.extract_file_name  # 'matbench_dielectric.json'
        # file_name_base = os.path.splitext(self.file_name)[0]

        if all([os.path.exists(self.pymatgen_json_file_path), os.path.exists(self.file_path), not overwrite]): #F
            self.info("Found '%s' of structures." % self.pymatgen_json_file_path)
            return self

        self.info("Load dataset '%s' to memory..." % self.dataset_name)
        data = load_json_file(os.path.join(self.data_directory, file_name_download)) 

        self.info("Process database with %s and columns %s" % (data.keys(), data["columns"]))
        data_columns = data["columns"] #['structure','en_labels']
        index_structure = 0
        for i, col in enumerate(data_columns):
            if col == file_column_name:  # ’structure‘
                index_structure = i
                break
        py_mat_list = [x[index_structure] for x in data["data"]]

        self.info("Write structures or compositions '%s' to file." % self.pymatgen_json_file_path)
        save_json_file(py_mat_list, self.pymatgen_json_file_path)
        df_dict = {"index": data["index"]}
        for i, col in enumerate(data_columns):
            if i != index_structure:
                df_dict[col] = [x[i] for x in data["data"]]
        df = pd.DataFrame(df_dict)

        self.info("Write dataset table '%s' to file." % self.file_name)
        df.to_csv(self.file_path)
        return self
