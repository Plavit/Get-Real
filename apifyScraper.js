const Apify = require('apify');

function removeChars(string){
    var find = '\n';
    var re = new RegExp(find, 'g');
    string = string.replace(re, '');

    string = string.trim();
    return string;
}

Apify.main(async () => {
    const input = await Apify.getInput()
    var advertTypeList = ["prodej", "pronajem", "spolubydleni"];
    var propTypeList = ["byt", "dum", "pozemek", "garaz", "kancelar", "nebytovy-prostor", "chata-chalupa"];    

    for(var advertType in advertTypeList)
    {
        for(var propType in propTypeList)
        {
            let pageNumber = 1;
            var goOn = true;
            while (goOn === true)
            {
                const requestQueue = await Apify.openRequestQueue();
                var urlString = 'https://www.bezrealitky.cz/vypis/nabidka-'+advertTypeList[advertType]+'/'+propTypeList[propType]+'?page=' + String(pageNumber);
                await requestQueue.addRequest
                ({ 
                    url: urlString,
                    userData: {label: "START"} 
                });

                const proxyConfiguration = await Apify.createProxyConfiguration()

                
                const crawler = new Apify.PuppeteerCrawler({
                    requestQueue,
                    proxyConfiguration,
                    maxRequestsPerCrawl: 50,
                    handlePageFunction: async ({ request, page, body }) => {
                        console.log(`Processing ${request.url}...`);
    
                        if (request.userData.label === "START"){
                            const infos = await Apify.utils.enqueueLinks({
                                page,
                                requestQueue,
                                selector: '.product__link.js-product-link',
                            });

                            const pageCount = await page.$$eval('ul.pagination li', (els) => {
                                const targetEl = els[els.length - 2];
                                return Number(targetEl.textContent);
                            })

                            console.log(`Page count: ${pageCount}`)
                            if(pageCount === pageNumber){goOn = false;}
                            
                            var keyImage = "Start" + String(pageNumber)
                            await Apify.utils.puppeteer.saveSnapshot(page, { key: keyImage})
                        }else{
                            console.log(`Processing ${request.url}...`);

                            var price = await page.$eval('.detail-price', (el) => el.textContent);
                            var find = '\n';
                            var re = new RegExp(find, 'g');
                            price = price.replace(re, '');
                            find = ' ';
                            re = new RegExp(find, 'g');
                            price = price.replace(re, '');    
                            
                            var name = await page.$eval('.col h1', (el) => el.textContent);

                            var adress = await page.$eval('.col.col-12 h2', (el) => el.textContent);
                            var adressList = adress.split(", ");
                            var street = adressList[0];
                            street = removeChars(street);
                            var town = adressList[1];
                            var region = adressList[2];
                            region = removeChars(region);

                        var dispozition = await page.$$eval('#detail-parameters .row.pl-md-4  .col.col-6.param-value', (els) => {
                            return els[2].textContent;
                        })
                        rooms = removeChars(dispozition);

                        var dispozition = await page.$$eval('#detail-parameters .row.pl-md-4  .col.col-6.param-value', (els) => {
                            return els[3].textContent;
                        })
                        state = removeChars(dispozition);

                        var dispozition = await page.$$eval('#detail-parameters .row.pl-md-4  .col.col-6.param-value', (els) => {
                            return els[4].textContent;
                        })
                        surface = removeChars(dispozition);

                        var dispozition = await page.$$eval('#detail-parameters .row.pl-md-4  .col.col-6.param-value', (els) => {
                            return els[7].textContent;
                        })
                        ownerType = removeChars(dispozition);

                        var dispozition = await page.$$eval('#detail-parameters .row.pl-md-4  .col.col-6.param-value', (els) => {
                            return els[8].textContent;
                        })
                        buildingType = removeChars(dispozition);


                            await Apify.pushData({
                                url: request.url,
                                name: name,
                                price: price,
                                advertType: advertTypeList[advertTypeList],
                                propTypeList: propTypeList[propTypeList],
                                street: street,
                                town: town,
                                region: region,
                                rooms: rooms,
                                state: state,
                                ownerType: ownerType,
                                surface: surface,
                                buildingType: buildingType
                            });
                            //COMING SOON
                        }
                    },
                });
                
                await crawler.run();
                pageNumber ++;
            }
        }
    }
    console.log('Crawler finished.');
});
