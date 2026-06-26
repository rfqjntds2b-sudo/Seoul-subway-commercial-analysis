# Seoul Transit & Commercial Inflow Cost-Benefit (C/P) Analysis

This repository contains the data analysis, spatial algorithms, and presentation layout for evaluating commercial zone efficiency in Seoul. By merging subway/bus alighting population (crowd density as **Cost**) and local restaurant/pub density (choice options as **Benefit**), we compute a **Congestion Cost-Benefit (C/P) Index** to identify "hidden gems" (high benefit, low cost alternative zones).

---

## 1. Project Background (Context)
* **Situation**: Map platforms (Naver Maps, KakaoMap, etc.) provide abundant food information and pathfinding. People use these platforms to find locations for weekends and Friday nights.
* **Complication**: Relying on simple hot-place recommendations leads users to overcrowded spots (e.g., Gangnam, Hongdae) with extreme queues, transit congestion, and a degraded user experience (UX). Currently, there is no unified index assessing crowd density vs. shop volume to find pleasant but rich commercial zones.
* **Question**: How can we merge public transit flow and shop density data to suggest alternative, high-value, low-crowd commercial zones?
* **Solution**: Build a **Congestion Cost-Benefit (C/P) Index** using spatial matching (Haversine 500m radius scans) of subway stations and surrounding food/drink venues.

---

## 2. Methodology
1. **Data Preprocessing**:
   - **Subway**: Monthly transit logs and coordinate mappings (filtered for May 2026).
   - **Bus**: Annual boarding logs and bus stop GPS nodes.
   - **Shops**: Local business directory containing coordinates of restaurants, cafes, and pubs in Seoul.
2. **Spatial Matching**:
   - For each subway station, calculate the total bus alighting flow and food shop counts within a **500-meter radius** using the Haversine distance formula.
3. **C/P Index Equation**:
   $$\text{C/P Index} = \frac{\text{Number of Food/Drink Shops within 500m (Benefit)}}{\text{Combined Subway and Bus Alighting Inflow (Cost)} + 1} \times 10,000$$

---

## 3. Directory Structure
```text
ABCD/
├── .gitignore                                 # Files excluded from Git pushes
├── README.md                                  # Project explanation (this file)
├── seoul_subway_analysis.ipynb                 # Main analysis and mapping Jupyter Notebook
├── project.ipynb                              # Preprocessing and map overlay Notebook
├── project_context.txt                        # Project background context
├── pencil-new.pen                             # [Excluded] Slide design file for Pencil.dev (1920x1080)
├── generate_dark_plot_en.py                   # Script to generate the English dark-theme plot
├── subway_bus_shop_merged_result_optimized.csv # Processed final dataset
├── subway_location_data_2023_2026.csv         # Subway coordinate datasets
├── bus_location_data.csv                      # Bus node datasets
├── Seoul_subway_data_2023_2026.csv            # Subway transit datasets (subset)
├── images/                                    # [Excluded] Local folder for generated plot assets
├── backup_scratch/                            # [Excluded] Temporary scratch files
└── presentation_materials/                    # [Excluded] Local PPTX, PDF, and scripts
```

---

## 4. Key Findings

### Alternative Zone (Hidden Gems) - 2nd Quadrant
* **Characteristics**: Low transit crowd flow (Cost) and rich shop counts (Benefit).
* **Representative Areas**: **Sangsu Station (C/P: 18.14)**, **Songpanaru Station (C/P: 13.15)**, **Seokchongobun Station (C/P: 10.60)**, Mangwon Station, Itaewon Station.
* **Visualization**: Plot representation is saved under `images/cp_matrix_dark.png`.

### Saturated Zone (Traditional Hot Spots) - 1st/4th Quadrant
* **Characteristics**: Extremely high crowd flow (Cost), making the experience crowded despite rich options.
* **Representative Areas**: Gangnam Station, Hongdae Station, Seongsu Station, Sinchon Station, Yeouido Station.
