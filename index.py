from selenium import webdriver
from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

WORDS = ['river', 'water', 'ocean', 'liquid', 'stream', 'lake', 'wave', 'pool']

driverPath = './drivers/chromedriver_win32/chromedriver.exe'
url = 'https://www.behindthename.com/'
driver = webdriver.Chrome(driverPath)

driver.get(url)
timeout = 3

# mainSearch = driver.find_element_by_id('main_search')
countryTable = driver.find_elements_by_class_name('usagelinks')[0]
englishNamesLink = countryTable.find_elements_by_css_selector("*")[0].find_elements_by_css_selector("*")[0]
englishNamesLink.click()
""" 
genderSelector = driver.find_elements_by_class_name('nb-quickselect')[0]
select = Select(genderSelector)

# select by visible text
select.select_by_visible_text('Masculine')
 """

outputFile = open('./index.html', 'w', encoding="utf-8")
outputFile.write('''
<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="X-UA-Compatible" content="ie=edge">
	<title>Document</title>
	<style>
		* {
			font-family: sans-serif
		}

		a {
			text-decoration: none;
			color: cornflowerblue;
		}

		body {
			width: 60vw;
			margin: auto
		}

		.listname>a {
			font-family: 'Times New Roman', Times, serif;
			text-decoration-style: wavy;
			font-size: 1.4rem;
		}

		.masc {
			font-size: 1rem;
			font-weight: bold;
			margin: 10px;
			color: rgb(22, 118, 196)
		}

		.fem {
			color: rgb(206, 86, 170);
			font-size: 1rem;
			font-weight: bold;
			margin: 10px;

		}

		.name-div {
			margin: 20px;
			font-size: .9rem;
			color: rgb(73, 73, 73)
		}

		.listusage {
			color: red
		}

		.header {
			margin: auto;
			background: rgb(93, 123, 177);
			position: -webkit-sticky;
			position: sticky;
			padding-top: 20px;
			padding-bottom: 20px;
			top: 0px;
		}
		.header > div {
			margin: 0px;
			font-size: .8rem;
			text-align: center;
			color: rgb(212, 212, 212)
		}
		.header > div > span {
			color: white
		}
        .found-word{
			background-color: rgb(255, 239, 147);
			margin: 0px;
			padding: 0px;
		}

		@media only screen and (max-width: 600px) {
			* {
				margin: 0px;
			}

			body {
				width: 90vw;
			}
		}
	</style>
</head>

<body>
	<div class="header">
		<div>
			Found with a query on 'https://www.behindthename.com/'
		</div>
		<div>
			search words: <span> 'river' 'water', 'ocean', 'liquid', 'stream', 'lake', 'wave', 'pool'</span>
		</div>
		<div>
			- galib
		</div>
	</div>


''')


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
                toBeWritten = nameDiv.get_attribute('innerHTML').replace(word, f'''<span class="found-word"> {word} </span> ''')

                outputFile.write('<div class="name-div">')
                outputFile.write('\n')
                outputFile.write('\t')
                outputFile.write(toBeWritten)
                outputFile.write('\n')
                outputFile.write('</div>')
                outputFile.write('\n')

    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'pagination'))
    WebDriverWait(driver, timeout).until(element_present)

    paginationDiv = driver.find_elements_by_class_name('pagination')[0] # since there are two same pagination divs

    all_a_in_pagination = paginationDiv.find_elements_by_css_selector('a')
    for a in all_a_in_pagination:
        aContent = a.get_attribute('innerHTML').lower() 
        if 'next' in aContent and 'page' in aContent:
            # click
            a.click()
            
            findWordInPage()

findWordInPage()

outputFile.write('''

	<script>
	
		nameSpans = Array.from(document.querySelectorAll('.listname'))
		nameSpans.forEach(nameSpan => {
			const a = nameSpan.children[0]
			a.innerHTML = a.innerHTML.toLowerCase()
			a.style.textTransform = 'capitalize'
		})

	</script>
</body>

</html>

'''
)

outputFile.close()
driver.close()
