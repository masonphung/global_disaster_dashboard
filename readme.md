# Global Disaster Dashboard
## Macquarie DataViz 2024 Challenge Winner for the Best Interactive Visualization award.

- [Link](https://sdgdashboard.masonphung.com) to The Online Dashboard: 
- We suggest to run the dashboard in Google Chrome/firefox for the best experience.
- Follow `project-description.ipynb` to run the dashboard locally.

### Let's take a look on your mobile device !

<img src="assets/images/teamA-dashboard-QR.png" width="145">

### Introduction - A dash dashboard presents the global disasterous status
Our project focuses on developing an interactive dashboard that analyzes global disaster data, sourced from the EM-DAT database, to visualize the impacts of climate-related disasters. By tracking key metrics such as total deaths, affected populations, and economic losses, the dashboard provides valuable insights into disaster trends. These insights support the United Nations' SDG Goal 13.1, which aims to strengthen resilience and adaptive capacity to climate-related hazards. Through this tool, policymakers and disaster management agencies can make informed decisions, helping to reduce the risks associated with climate change and enhance global preparedness for future disasters.

<img src="assets/images/tsunami-icegif-9.gif" width="990">


### Data: EM-DAT Public Table
The data used for the dashboard is the EM-DAT Public Table of the International Disaster Database. Additional information could be found on EM-DAT [documentation website](https://doc.emdat.be/docs/data-structure-and-content/general-definitions-and-concepts/).

> *EM-DAT was designed in 1988 based on an anthropocentric vision of disasters and emergencies. It considers disasters to be events involving an unexpected and overwhelming harmful impact on human beings.*
    *The EM-DAT Public Table is a comprehensive, publicly accessible database that tracks the occurrence and impact of major natural and technological disasters worldwide. Managed by the Centre for Research on the Epidemiology of Disasters (CRED), it includes detailed information on disaster events such as dates, locations, types, and the resulting human and economic losses.*

EM-DAT granted free access for [non-commercial use](https://doc.emdat.be/docs/legal/terms-of-use/).

### Key Features

![](assets/images/dashboard_cap.jpg)

- **Python programmed**: The dashboard built with Python allow easy future development, cross-platform accessibility, and efficient data processing and updates.  
- **User-Friendly Interface**: Offers an interactive, easy-to-use platform for policymakers, researchers, and disaster management teams.
- **Data-Driven Decisions**:  Eye-catching visuals and interactive plots, combined with a wide range of filters, allow users to explore disaster impacts, identify high-risk areas, and assess trends, supporting effective disaster preparedness and risk reduction.
- **An SDG 13 approach**: By providing real-time insights into climate-related disasters, enabling decision-makers to strengthen resilience, improve disaster preparedness, and reduce the risks associated with climate change impacts.
- **Climate-Related Focus**: By highlighting climate-related disasters, the dashboard underscores the growing impact of climate change on global vulnerabilities, reinforcing the urgency for adaptation and mitigation efforts.

### Last update
- Full update logs: [Update log](/update_log.txt)

### Repository Tree  
    ├─ assets/ - Dashboard visual components
    │  ├─ images/
    │  ├─ bootstrap.css - Bootstrap CSS theme for the dashboard
    ├─ dataset/
    │  ├─ backups/ : Including raw and backup datas
    │  │  └─ ...
    │  └─ cleaned_emrat.xlsx : Cleansed data
    ├─ .gitignore
    ├─ dash_app.py
    ├─ data_cleaning.py: Raw data cleaning process
    ├─ project-description.ipynb: Full project description and dashboard local run tutorial
    ├─ readme.md
    ├─ requirements.txt
    ├─ update_log.txt
    ├─ utils.py
    └─ working_process.ipynb

### Special thanks to
- The International Disaster Database EM-DAT for the Public Table about global disaster. Find out about EM-DAT and the Public Table [here](https://doc.emdat.be/docs/data-structure-and-content/emdat-public-table/).
- [Bootswatch](https://bootswatch.com) bootstrap template theme by Thomas Park. We make a considerable amount of changes to customize the theme and make sure the final theme works well.
