from fasthtml.common import *
from monsterui.all import *
import requests
from pydantic import BaseModel
from urllib3.exceptions import HTTPError as BaseHTTPError


hdrs = Theme.rose.headers()

app,rt = fast_app(hdrs=hdrs)

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
    
@rt('/')
def index():
    try:        
        search_form = Form(method="get", action="/search", cls="flex items-end gap-2 w-full")(
            LabelInput("", id="search-input", name="character", placeholder="Enter Card name...", cls="w-[92%]"),   
            Button("Submit Form", cls=(ButtonT.primary, "w-[8%]"))
        )

        return Titled(Center("MTG Card Viewer"),
            Br(),
            search_form,
            Br(),
            RecentChips()
        )
            
        
    except BaseHTTPError as e:
        return Titled(Center("MTG Card Viewer"),
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
            
            search_form = Form(method="get", action="/search", cls="flex items-end gap-2 w-full")(
                        LabelInput("", id="search-input", name="character", placeholder="Enter Card name...", cls="w-[92%]"),   
                        Button("Submit Form", cls=(ButtonT.primary, "w-[8%]"))
            )
                    
            return Br(),Titled(f"Results for character: {character.capitalize()}",
                Br(),
                search_form,
                Br(),
                A("← Back to Index", href="/", cls="text-base"),
                Br(),Br(),
                Grid(*results,cls="grid justify-center")
            )

    except BaseHTTPError as e:
        return Card(
                H1("There as an error"),
                P(f"Error {e}")
            )

if __name__ == "__main__":
    serve()