# TuniSci: Ranking of scholars at Tunisian universities based on h-index and i10-index
By ***Mohamed Fares Landoulsi*** (University of Tunis El Manar, Tunisia)

**The Ranking is live at https://Frostbite22.github.io/TuniSci/ranking.html.**

Scientists always need to locate their position in the research landscape of their community so that they can assess their career and envision future directions for their work by seeing what their peers are doing. Tunisian scientists are not an exception to this rule. In this context, several bibliometric studies have been conducted to identify the main local scientists and trends in various research fields in Tunisia, particularly Chemistry [1], Infectious Diseases [2], Community Health [3], General Surgery [4], and so on. When robust measures allowing the quantitative and qualitative assessment of scientists, mainly h-index, have appeared since 2005 [5], a new trend of using such metrics to rank scientists has appeared allowing the generation of various rankings for scientists by discipline and country, especially in the developed nations [6]. In Tunisia, the first h-index ranking has been created in 2014 featuring local and expatriate scientists [7]. It was based on extracting all Tunisian surnames from the phone directory and then using Google Scholar to scrape all the names of scientists that are likely to be Tunisian citizens. The list is later filtered to include only highly-cited scientists (h-index >= 15) and then verified by hand to verify its accuracy. Despite the added value of this work, it mistakenly included several non-Tunisian scientists and discarded influential Tunisian scientists. A series of disciplinary rankings have been done later to solve this problem [8-9]. In 2017, a second generation of h-index rankings has appeared in Tunisia with the creation of a semi-automated ranking named *TunSci* [10]. This ranking adds influential scientists to an Excel spreadsheet by hand (h-index >= 20 for local scientists and h-index >= 30 for expatriate scientists). Then, the Excel spreadsheet is linked to the public Google Scholar profiles of these scientists using the Microsoft .NET Framework and subsequently used to automatically update the ranking on a regular basis by scraping Google Scholar. Although these works achieved a certain recognition, they had several limitations  that led to their interruption in 2019:
* Comparing scientists from different fields is not appreciated, particularly as several areas are more likely to be cited than other ones [11].
* Older scientists are more likely to achieve higher h-index than younger ones [12].
* Ranking scientists by numbers from first to last is quite humiliating for scientists at the least positions and can be a source for disencouraging scientists rather than encouraging them to progress in their careers.
* Curating rankings by hand is a long task that requires long-term engagement.

Here, I propose TuniSci as a new ranking that automatically create a ranking of local Tunisian scientists by scraping their public Google Scholar profiles. This project's intent is to refect the real impact and contribution of Tunisian universities on research in general and on the qualities of higher education in Tunisia. Such a ranking will solve problems related to the sustainability of the classification. To tackle social problems related to previous h-index rankings, I will provide four measures that assess different aspects of scientific achievements for every considered scientist:
* **h-index:** The h-index is an author-level metric that measures both the productivity and citation impact of the publications, initially used for an individual scientist or scholar [5]. The h-index correlates with obvious success indicators such as winning the Nobel Prize, being accepted for research fellowships and holding positions at top universities [5]. This metric is defined as *h* where *h* of the publications have each received *h* citations or more and where the remaining publications have received *h* citations or less. 
* **i10-index:** The number of publications that have been each cited ten times or more. i10-index is highly correlated with h-index [13]. Consequently, scientists with higher i10-index are more likely to increase their h-index soon.
* **5-year h-index:** This metric is defined as *h* where *h* of the publications have each received *h* citations for the last five years or more and where the remaining publications have received *h* citations or less for the last five years. Thanks to its five-year window for citations, this measure favors young and active scientists at the expense of retired and inactive ones.
* **5-year i10-index:** The number of publications that have been each cited ten times or more for the last five years.

To prevent any mistaken interpretation of the ranking, I decided to eliminate putting ranks for every scientist. Scientists are initally visualized in a random way. Any user can sort the scientists based on a metric by clicking on the header cell of the corresponding column. Just for reference, Hirsch reckons that after 20 years of research, an h-index of 20 is good, 40 is outstanding, and 60 is truly exceptional [5]. But, if you work on a research field with limited citation impact and important publishing delays, even a smaller number can be excellent.



## References
1. Hammouti, B. (2010). Comparative bibliometric study of the scientific production in Maghreb countries (Algeria, Morocco and Tunisia) in 1996-2009 using Scopus. *Journal of Materials & Environmental Science*, 1(2), 70-77.
2. Rouis, S., Melki, S., Rouis, H., & Nouira, S. (2019). Disciplinary and thematic mapping of Maghreb publications in" infectiology". Bibliometric study (Tunisia, 2010-2014). *La Tunisie medicale*, 97(8-9), 931-944.
3. Alaya, B. (2018). Bibliometrics of Tunisian publications in preventive and community medicine, indexed in the Medline database (1975-2014). *La Tunisie Medicale*, 96(10-11), 719-730.
4. Azzaza, M., Melki, S., Nouira, S., & Khelil, M. (2019). Bibliometrics of Tunisian publications in" General Surgery"(Medline, 2009-2018). *La Tunisie medicale*, 97(7), 833-841.
5. Hirsch, J. E. (2005). An index to quantify an individual's scientific research output. *Proceedings of the National academy of Sciences*, 102(46), 16569-16572.7
6. Cronin, B., & Meho, L. (2006). Using the h‐index to rank influential information scientists. *Journal of the American Society for Information Science and technology*, 57(9), 1275-1278.
7. Turki, H., & Turki, M. (2014). *Ranking of Tunisian Scientists According to Their Efficient Productivity. An Overview of Scientific Research Output in Tunisia*. GRIN Verlag.
8. Turki, H. (2016). An overview of the main Tunisian scientists in Chemistry and Materials Science. *Journal of Materials and Environmental Science*, 7(4), 1064-1071.
9. Turki, H. (2015). *Leading Tunisian scientists in Mathematics, Computer Science and Engineering. An Overview*. GRIN Verlag.
10. Turki, H. (2017). *TunSci: Semi-automated Google Scholar based h-index ranking for Tunisian scientists*. Webometrics.info.
11. Alonso, S., Cabrerizo, F. J., Herrera-Viedma, E., & Herrera, F. (2009). h-Index: A review focused in its variants, computation and standardization for different scientific fields. *Journal of informetrics*, 3(4), 273-289.
12. Kelly, C. D., & Jennions, M. D. (2006). The h index and career assessment by numbers. *Trends in Ecology & Evolution*, 21(4), 167-170.
13. McCoy, A. B., Sittig, D. F., Lin, J., & Wright, A. (2019). Identification and ranking of biomedical informatics researcher citation statistics through a Google Scholar scraper. In *AMIA Annual Symposium Proceedings* (Vol. 2019, p. 655). American Medical Informatics Association.
14. Pan, R. K., & Fortunato, S. (2014). Author Impact Factor: tracking the dynamics of individual scientific impact. *Scientific reports*, 4(1), 1-7.


## Scope 
This project is build by scraping the google scholars for Tunisian university. It contains 2130 scholars from different univerities, with different research fields and interests.

## Significatant statistics 
Average h-index : 8.1

## Things to be done in this project ( contributions are welcomed )
#### Average h-index by research field ( most successful fields )
#### standard deviation from all authors ( we have many with zero publications ) 
#### number of scholars working on each field 
