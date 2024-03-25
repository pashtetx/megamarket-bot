from playwright import async_api
from bs4 import BeautifulSoup
from typing import TypedDict, List, AsyncGenerator, AsyncIterator

class ShopDict(TypedDict):
    title: str
    url: str

class ProductDict(TypedDict):
    title: str
    url: str
    price: int
    shop: ShopDict
    img: str = None
    cashback: int = None
    

def parse_product(product_html, parse_all: bool = False) -> ProductDict:
    """ Return ProductDict from Product HTML data
        product_html - HTML product text
        parse_all - If False function return 
    """
    product_title = product_html.find("div", {"class":"item-title"})
    product_a = product_title.find("a")
    product_title = product_a.attrs["title"]
    product_url = product_a.attrs["href"]
    product_img = product_html.find("img", attrs={"class":"lazy-img"})
    if product_img:
        product_img = product_img.attrs["src"]
    product_price = product_html.find("div", attrs={"class":"item-price"}).getText().replace(" ", "").replace("₽", "")
    cashback = product_html.find("span", attrs={"class":"bonus-percent"})

    shop_a = product_html.find("a", {"class":"merchant-info"})
    if not shop_a:
        return
    shop_url = shop_a.attrs["href"]
    shop_title = shop_a.find("span")
    
    shop = ShopDict(title=shop_title.getText(), url=shop_url)
    
    if cashback:
        cashback = int(cashback.getText().replace("%", ""))
    if not parse_all and not cashback:
        return
    return ProductDict(title=product_title, img=product_img, url=product_url, price=int(product_price), cashback=cashback, shop=shop)



async def get_products(html: str, parse_all: bool = False) -> List[ProductDict]:
    """ Return products list from a current page
        html - str HTML text from megamarket catalog
        parse_all - bool, if True function return products without cashback else function return product only with cashback
    """
    soup = BeautifulSoup(html, "lxml")
    product_block = soup.find("div", attrs={"class":"catalog-items-list"})
    if not product_block:
        raise StopAsyncIteration()
    products = product_block.find_all("div", {"class":"catalog-item"})
    products_list = []
    for product in products:
        product_obj = parse_product(product_html=product, parse_all=parse_all)
        if product_obj:
            products_list.append(product_obj)
    
    return products_list

async def parse_products(url: str, browser, start_page: int = 1, parse_all: bool = False, wait_until: str = "commit") -> AsyncIterator[AsyncGenerator]:
    """ Parsing product from megamarket.ru 
        start_page - int, page from which to start parsing
        parse_all - bool, if True function return products without cashback else function return product only with cashback
        wait_until - str, event load page. more: https://playwright.dev/python/docs/release-notes#behavior-change
    """

    page_num = start_page

    while True:
        page = await browser.new_page()
        resp = await page.goto(url + f"page-{page_num}/", wait_until=wait_until)
        content = await resp.text()
        await page.close()
        yield await get_products(content, parse_all=parse_all)
        page_num += 1