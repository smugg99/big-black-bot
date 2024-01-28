import os
import random
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from interactions import Client, Intents, SlashContext, listen, slash_command, Embed, Color
from dotenv import load_dotenv

bot = Client(intents=Intents.DEFAULT)
base_url = "https://blackcockpictures.com/category/black-cock-pictures/"

async def extract_image_sources(url):
	async with async_playwright() as p:
		browser = await p.chromium.launch()
		context = await browser.new_context()
		page = await context.new_page()

		await page.goto(url)
		await page.wait_for_selector(".gallerywp-grid-post")

		html_content = await page.content()

	soup = BeautifulSoup(html_content, "html.parser")

	post_elements = soup.find_all("div", class_="gallerywp-grid-post")
	image_sources = [post.select_one(".gallerywp-grid-post-thumbnail-img")["src"] for post in post_elements
					 if post.select_one(".gallerywp-grid-post-thumbnail-img")]

	return image_sources

@slash_command(name="givemeanigga", description="Gives you a nigga :)")
async def give_me_a_nigga(ctx: SlashContext):
	if ctx.channel.nsfw:
		random_page_number = random.randint(1, 100)
		image_sources = await extract_image_sources(base_url + f"page/{random_page_number}")

		embed = Embed(
			title="Look at that gyyaat nigga 😛😛😛",
			description="",
			color=0
		)
		
		embed.set_image(url=random.choice(image_sources))

		await ctx.send(embed=embed)
	else:
		await ctx.send("This command can only be used in NSFW channels nigga 💀💀💀")

@listen()
async def on_ready():
	print("Logged in")

def main():
	load_dotenv(".env")
	bot.start(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
	main()
