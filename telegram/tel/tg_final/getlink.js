let array = []
linklist = document.querySelector("#home-section > div > div > div:nth-child(4) > div").children
for(let i = 1; i <= linklist.length; i++){
    jsPath = "#home-section > div > div > div:nth-child(4) > div > div:nth-child(" + i + ") > div > a"
    link = document.querySelector(jsPath).getAttribute('href')
    array.push(link)
}
console.log(array)
