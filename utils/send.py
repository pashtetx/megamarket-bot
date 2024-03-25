from aiogram import Bot
from megamarket.queries import ProductDict, parse_products
from db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


async def send_product(bot: Bot, chat_id: int, product: ProductDict) -> None:
    """ Format ProductDict to a text
        :bot param: - Bot, aiogram bot
        :chat_id param: - int, chat_id to send a message
        :product param: ProductDict, for format message
    """
    
    text = "<a href=\"https://megamarket.ru{url}\"><b>{title}</b></a>\n\n💵 Стоимость: {price} ₽\n💰 Кешбек: {cashback}%\n🔰 Стоимость с кешбеком: {price_with_cashback} ₽\n 🏬 Магазин: <a href=\"https://megamarket.ru{shop_url}\">{shop_title}</a>".format(
        title=product.get("title"), 
        price=product.get("price"), 
        cashback=product.get("cashback"), 
        url=product.get("url"),
        shop_url=product.get("shop").get("url"),
        shop_title=product.get("shop").get('title'),
        price_with_cashback=round(product.get("price") - (product.get("cashback") / 100) * product.get("price"))
    )
    await bot.send_photo(chat_id=chat_id, photo=product.get("img"), caption=text)


async def send_products(bot: Bot, session: AsyncSession, chat_id: int, url: str, cashback: int, browser) -> None:
    """ Generate products and send that
        :bot param: - Bot, aiogram bot
        :chat_id param: - int, chat_id to send a message
    """
    async for products in parse_products(url=url, browser=browser):   
        user = await User.objects.get(session, telegram_id=chat_id)
        if not user.is_parsing:
            break
        else:
            session.expire(user)
        for product in products:
            if product.get("cashback") >= cashback:
                await send_product(bot=bot, chat_id=chat_id, product=product)