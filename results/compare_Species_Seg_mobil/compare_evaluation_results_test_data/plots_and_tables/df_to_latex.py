import pandas as pd
import numpy as np

# Read the data from your text files
df1 = pd.read_csv(r'C:\Users\janni\Dokumente\Masterarbeit\python_scripts\final_python_scripts\master-thesis\results\compare_Species_Seg_mobil\compare_evaluation_results_test_data\plots_and_tables\YOLO_base_metrics.txt',
                  sep='\t')
df2 = pd.read_csv(r'C:\Users\janni\Dokumente\Masterarbeit\python_scripts\final_python_scripts\master-thesis\results\compare_Species_Seg_mobil\compare_evaluation_results_test_data\plots_and_tables\SpeciesSeg_metrics.txt',
                  sep='\t')


# Function to convert a dataframe to LaTeX table format
def df_to_latex(df):
    latex = df.to_latex(index=False, escape=False)
    return latex


df_merged = df1.merge(df2, on=['class_index', "species"])

df_merged = df_merged.drop('class_index', axis=1)

df_merged_ordered = df_merged[['species', 'f1_mask_n_base', 'f1_mask_n_weighted_tuned',
                               'map_50_95_mask_n_base', 'map_50_95_mask_n_weighted_tuned']]

df_merged_ordered[['f1_mask_n_base',
                   'f1_mask_n_weighted_tuned',
                   'map_50_95_mask_n_base',
                   'map_50_95_mask_n_weighted_tuned']] = df_merged_ordered[['f1_mask_n_base',
                                                                            'f1_mask_n_weighted_tuned',
                                                                            'map_50_95_mask_n_base',
                                                                            'map_50_95_mask_n_weighted_tuned']].round(3).astype(str)
print(df_merged_ordered)

latex_table = df_to_latex(df_merged_ordered)

print(latex_table)
