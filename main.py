from fasthtml.common import *
from monsterui.all import *
import requests
from pydantic import BaseModel
from urllib3.exceptions import HTTPError as BaseHTTPError

styles = (
    Theme.rose.headers(),
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-mfizz/2.4.1/font-mfizz.min.css")
)

app,rt = fast_app(hdrs=styles)

rcnt_srchs = []

def recent_searches(search: str):    
    rcnt_srchs.append(search)
    
    for item in rcnt_srchs:
        item_count = rcnt_srchs.count(item)
        if item_count > 1:
            rcnt_srchs.pop(rcnt_srchs.index((item)))
        if len(rcnt_srchs) > 20:
            rcnt_srchs.pop()
    return rcnt_srchs

def RecentChips():
    if not rcnt_srchs:
        return Span("No recent searches", cls="text-muted-foreground text-sm")
    return Card(
        CardHeader(
            CardTitle("Recent", cls="text-sm font-medium")
        ),
        CardBody(
            Div(
                *[A(s, href=f"/search?character={s}",
                    cls="inline-flex items-center px-3 py-1 rounded-full text-sm "
                        "bg-secondary text-secondary-foreground hover:bg-secondary/50 transition-colors")
                  for s in rcnt_srchs],
                cls="flex gap-2 flex-wrap"
            )
        ),
        cls="rounded-2xl shadow-sm"
    )

def LoveFooter():
    return Footer(cls="border-t py-6 mt-10")(
        Div(cls="uk-container uk-container-xl text-center text-l")(
            A(href="https://github.com/Lilithbtw/MTG_Wrapper", cls="underline decoration-pink-500 decoration-2 underline-offset-4 transition-all hover:underline-offset-2")(
                P("Made with ", Span("<3", cls="text-pink-500"), " Using...", cls="text-muted-foreground"),
            ),
            Div(cls="tech-stack")(
                I(cls="icon-docker text text-2xl",aria_label="Docker Icon"),
                I(cls="icon-python text-2xl",aria_label="Python Icon"),
            )
        )
    )

def SearchForm():
    search_form = Form(method="get", action="/search", cls="flex items-end gap-2 w-full")(
        LabelInput("", id="search-input", name="character", placeholder="Enter Card name...", cls="flex-1"),    
        Button("Submit", cls=(ButtonT.primary))
    )

    return search_form
    
@rt('/')
def index():
    try:

        return Titled("MTG Explorer - Index",
                Div(cls="flex flex-col min-h-screen")(
                    Main(cls="pb-32")(
                        Center("MTG Card Viewer"),
                        Br(),
                        SearchForm(),
                        Br(),
                        RecentChips()
                    ),
                    Div(cls="fixed bottom-0 left-0 w-full bg-background")(
                        LoveFooter()
                    )
                )
            )            
        
    except BaseHTTPError as e:
        return Titled("MTG Explorer - Error {e}", Center("MTG Card Viewer"),
            Br(),
            Card(
                H1("There as an error"),
                P(f"Error {e}")
            )
        )

@rt('/search')
def search(character: str = ""):
    if not character:
        return Redirect("/")
    
    recent_searches(character.capitalize())
    
    print(recent_searches)
    
    full_api_url = "https://api.scryfall.com/cards"
    
    class mtg_card(BaseModel):
        name: str
        img: tuple[str,str,str]
        mana_cost: str
        txt: str
        rarity: str
        type: str
    
    url = f"{full_api_url}/search?q={character}"
    
    try: 
        response = requests.get(url)
        
        data = response.json()
        
        magic_cards = []
        
        err_key = ""
        
        data_object = data["object"]
        
        print(data_object)
        
        if data_object == "error":
            err_key = data["details"]
            return Card(
                H1("There as an error, while fetching data"),
                P(f"Error: {err_key}")
            )
        else:
            for magic_card in data["data"]:
                if ("image_uris" and "oracle_text") in magic_card:
                    image_pre = magic_card["image_uris"]
                    
                    magic_cards.append(mtg_card(
                        name = magic_card["name"],
                        img = (
                            image_pre["small"], 
                            image_pre["normal"],
                            image_pre["large"]
                            ),
                        mana_cost = magic_card["mana_cost"],
                        txt = magic_card["oracle_text"],
                        rarity = magic_card["rarity"].capitalize(),
                        type = magic_card["type_line"]
                        )
                    )
                    
            print(len(data["data"]))
            
            if len(data["data"]) >= 3:
                results = [
                    Card(
                        H3(c.name),
                        Img(src=c.img[1], cls="rounded-lg"),
                        P(I(c.type)),
                        P(c.txt),
                        Footer(Small(f"Rarity {c.rarity}")),
                        cls="flex flex-col items-center text-center h-full" 
                    ) for c in magic_cards
                ]
            else:
                results = [
                    Center(Card(
                        H3(c.name),
                        Center(Img(src=c.img[1], cls="rounded-lg")),
                        P(I(c.type)),
                        P(c.txt),
                        Footer(Small(f"Rarity {c.rarity}")),
                        cls="flex-col items-center text-center h-full" 
                    )) for c in magic_cards
                ]
            
                    
            return Br(),Titled("MTG Explorer - Search",f"Results for character: {character.capitalize()}",
                Br(),
                SearchForm(),
                Br(),
                A("← Back to Index", href="/", cls="text-base"),
                Br(),Br(),
                Grid(*results,cls="grid justify-center"),
                Div(cls="bottom-0 left-0 w-full bg-background")(
                    LoveFooter()
                )

            )

    except BaseHTTPError as e:
        return Card(
                H1("There as an error"),
                P(f"Error {e}")
            )

if __name__ == "__main__":
    serve(host="0.0.0.0", port=5555)