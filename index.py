from selenium import webdriver
from selenium.webdriver.support.ui import Select

WORDS = ['river' 'water', 'ocean', 'liquid', 'stream', 'lake', 'wave', 'pool']

driverPath = './drivers/chromedriver_win32/chromedriver.exe'
url = 'https://www.behindthename.com/'
driver = webdriver.Chrome(driverPath)
driver.get(url)

# mainSearch = driver.find_element_by_id('main_search')
countryTable = driver.find_elements_by_class_name('usagelinks')[0]
englishNamesLink = countryTable.find_elements_by_css_selector("*")[0].find_elements_by_css_selector("*")[0]
englishNamesLink.click()

genderSelector = driver.find_elements_by_class_name('nb-quickselect')[0]
select = Select(genderSelector)

# select by visible text
select.select_by_visible_text('Masculine')


outputFile = open('./output.html', 'w', encoding="utf-8")

pageCount = 0
def findWordInPage():
    global pageCount

    pageCount += 1
    print('-----------------')
    print(f'Traversing page: {pageCount}')
    print('-----------------')

    # in the english names page
    namesDiv_all_inCurrentPage = driver.find_elements_by_class_name('browsename')
    for nameDiv in namesDiv_all_inCurrentPage:
        content = nameDiv.get_attribute('innerHTML').lower()
        for word in WORDS:
            if word in content:
                outputFile.write('<div>')
                outputFile.write('\n')
                outputFile.write('\t')
                outputFile.write(nameDiv.get_attribute('innerHTML'))
                outputFile.write('\n')
                outputFile.write('</div>')
                outputFile.write('\n')

    paginationDiv = driver.find_elements_by_class_name('pagination')[0] # since there are two same pagination divs
    all_a_in_pagination = paginationDiv.find_elements_by_css_selector('a')
    for a in all_a_in_pagination:
        aContent = a.get_attribute('innerHTML').lower() 
        if 'next' in aContent and 'page' in aContent:
            # click
            a.click()
            findWordInPage()

findWordInPage()

outputFile.close()
driver.close()
