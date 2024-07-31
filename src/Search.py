from bevyframe import *
from TheProtocols import User, Network
import requests

news_websites = {
    'www.cbsnews.com': 'CBS News',  # CBS is registered trademark of Paramount Global. HereUS Search is not affiliated with, endorsed by, or sponsored by Paramount Global.
    'www.foxnews.com': 'Fox News',  # Fox is registered trademark of Fox Corporation. HereUS Search is not affiliated with, endorsed by, or sponsored by Fox Corporation.
    'www.bbc.com': 'BBC News',  # BBC is registered trademark of BBC. HereUS Search is not affiliated with, endorsed by, or sponsored by BBC.
    'www.cnn.com': 'CNN',  # CNN is registered trademark of WarnerMedia. HereUS Search is not affiliated with, endorsed by, or sponsored by WarnerMedia.
    'www.reuters.com': 'Reuters',  # Reuters is registered trademark of Thomson Reuters. HereUS Search is not affiliated with, endorsed by, or sponsored by Thomson Reuters.
    'www.bloomberg.com': 'Bloomberg',  # Bloomberg is registered trademark of Bloomberg L.P. HereUS Search is not affiliated with, endorsed by, or sponsored by Bloomberg L.P.
    'www.nbcnews.com': 'NBC News',  # NBC is registered trademark of NBCUniversal. HereUS Search is not affiliated with, endorsed by, or sponsored by NBCUniversal.
    'www.usatoday.com': 'USA Today',  # USA Today is registered trademark of Gannett. HereUS Search is not affiliated with, endorsed by, or sponsored by Gannett.
    'www.theguardian.com': 'The Guardian',  # The Guardian is registered trademark of Guardian Media Group. HereUS Search is not affiliated with, endorsed by, or sponsored by Guardian Media Group.
    'www.nytimes.com': 'The New York Times',  # The New York Times is registered trademark of The New York Times Company. HereUS Search is not affiliated with, endorsed by, or sponsored by The New York Times Company.
    'www.washingtonpost.com': 'The Washington Post',  # The Washington Post is registered trademark of Nash Holdings. HereUS Search is not affiliated with, endorsed by, or sponsored by Nash Holdings.
    'www.wsj.com': 'The Wall Street Journal',  # The Wall Street Journal is registered trademark of Dow Jones & Company. HereUS Search is not affiliated with, endorsed by, or sponsored by Dow Jones & Company.
    'www.forbes.com': 'Forbes',  # Forbes is registered trademark of Forbes. HereUS Search is not affiliated with, endorsed by, or sponsored by Forbes.
    'www.businessinsider.com': 'Business Insider',  # Business Insider is registered trademark of Insider Inc. HereUS Search is not affiliated with, endorsed by, or sponsored by Insider Inc.
    'www.cnbc.com': 'CNBC',  # CNBC is registered trademark of NBCUniversal. HereUS Search is not affiliated with, endorsed by, or sponsored by NBCUniversal.
    'www.npr.org': 'NPR',  # NPR is registered trademark of National Public Radio. HereUS Search is not affiliated with, endorsed by, or sponsored by National Public Radio.
    'www.aljazeera.com': 'Al Jazeera',  # Al Jazeera is registered trademark of Al Jazeera Media Network. HereUS Search is not affiliated with, endorsed by, or sponsored by Al Jazeera Media Network.
    'www.euronews.com': 'Euronews',  # Euronews is registered trademark of Euronews. HereUS Search is not affiliated with, endorsed by, or sponsored by Euronews.
    'www.theatlantic.com': 'The Atlantic',  # The Atlantic is registered trademark of The Atlantic. HereUS Search is not affiliated with, endorsed by, or sponsored by The Atlantic.
    'www.ft.com': 'Financial Times',  # Financial Times is registered trademark of The Financial Times Ltd. HereUS Search is not affiliated with, endorsed by, or sponsored by The Financial Times Ltd.
    'deadline.com': 'Deadline',  # Deadline is registered trademark of Penske Media Corporation. HereUS Search is not affiliated with, endorsed by, or sponsored by Penske Media Corporation.
    'www.engadget.com': 'Engadget',  # Engadget is registered trademark of Verizon Media. HereUS Search is not affiliated with, endorsed by, or sponsored by Verizon Media.
    'www.webmd.com': 'WebMD',  # WebMD is registered trademark of WebMD. HereUS Search is not affiliated with, endorsed by, or sponsored by WebMD.
    'www.timesofisrael.com': 'The Times of Israel',  # The Times of Israel is registered trademark of The Times of Israel. HereUS Search is not affiliated with, endorsed by, or sponsored by The Times of Israel.
}  # This list is created by adding the news websites I have seen while at development. Create issue to have more added.

result = lambda x, u: Container(
    selector='the_box result',
    childs=x,
    onclick=f"window.location.href='{u}'",
    margin=Margin(bottom=Size.pixel(10)),
    width=Size.max_content,
    cursor=Cursor.pointer,
    max_width=substract_style(Size.Viewport.width(100), Size.pixel(60)),
)


web_result = lambda x: result([
    Label(Bold(x.title), font_size=Size.Relative.font(1.2), margin=Margin(bottom=Size.Relative.font(-1))),
    Label(x.url, font_size=Size.Relative.font(0.8), color="#808080", margin=Margin(bottom=Size.Relative.font(-1)), selector="url"),
    Label(x.description, font_size=Size.Relative.font(1)),
], x.url)

article_result = lambda x: result([
    Label(
        innertext=f'Article from {news_websites[x.url.split('/')[2]]}',
        font_size=Size.Relative.font(0.8),
        color="#808080",
        margin=Margin(bottom=Size.Relative.font(-1)),
        selector="url"
    ),
    Label(
        Bold(x.title.removesuffix(news_websites[x.url.split('/')[2]]).removesuffix(' - ').removesuffix(' : ')),
        font_size=Size.Relative.font(1.2),
        margin=Margin(bottom=Size.Relative.font(-0.7))
    ),
    Label(f"{x.description.removesuffix('.')}... <i>Read More</i>", font_size=Size.Relative.font(1)),
], x.url)

user_result = lambda x, h, n: result([
    Line([
        Image(
            src=x.profile_photo,
            alt="Profile Photo",
            height=Size.Relative.font(0.9),
            width=Size.Relative.font(0.9),
            border_radius=Size.percent(50),
            margin=Margin(right=Size.Relative.font(0.3))
        ),
        Bold(x)
    ], margin=Margin(bottom=Size.Relative.font(-1)), font_size=Size.Relative.font(1.2)),
    Label(h, margin=Margin(bottom=Size.Relative.font(-0.5))),
] + [
    Label(f'<b>{i[0]}:</b> {i[1]}', margin=Margin(bottom=Size.Relative.font(-1 if i[0] != 'Time Zone' else 0)))
    for i in [
        [
            'Subscription',
            (n.membership_plans[x.id] if float(n.version) >= 3.1 else ['Free', 'Plus', 'Pro', 'Ultra'])[x.plus]
        ],
        ['Birthday', x.birthday if x.birthday.replace('*', '') != '' else 'Hidden'],
        ['Country', x.country if x.country.replace('*', '') != '' else 'Hidden'],
        ['Gender', x.gender if x.gender.replace('*', '') != '' else 'Hidden'],
        ['Phone Number', x.phone_number if x.phone_number.replace('*', '') != '' else 'Hidden'],
        ['Zip Code', x.postcode if str(x.postcode).replace('*', '') != '' else 'Hidden'],
        ['Time Zone', 'GMT'+('+' if x.timezone >= 0 else '')+str(x.timezone)+':00'  if str(x.timezone).replace('*', '') != '' else 'Hidden']
    ]
], f"/@{h}")

github_result = lambda x: result([
    Line([Bold(x['full_name'])], margin=Margin(bottom=Size.Relative.font(-0.7)), font_size=Size.Relative.font(1.2)),
    Label(x['description'], margin=Margin(bottom=Size.Relative.font(-1))),
    Label(
        f'★ {x["stargazers_count"]} &nbsp; &nbsp; ◉ {x["watchers_count"]} &nbsp; &nbsp; ⑃ {x["forks_count"]}',
        margin=Margin(bottom=Size.Relative.font(-0.5))
    ),
    Label(f'<b>Language:</b> {x["language"]}', margin=Margin(bottom=Size.Relative.font(-1))),
    Label(f'<b>Open Issues:</b> {x["open_issues_count"]}', margin=Margin(bottom=Size.Relative.font(-1))),
    Label(f'<b>License:</b> {x["license"]["name"] if x["license"] is not None else "None"}')
], x['html_url'])

ap_note = lambda x, p: result([
    Container([
        '' if p.get('icon', {'url': None})['url'] is None else
        Container([
            Image(
                src=p.get('icon', {'url': None})['url'],
                alt='Profile Photo',
                height=Size.pixel(50),
                width=Size.pixel(50),
                border_radius=Size.percent(50)
            )
        ], css={'float': 'left'}),
        Container([
            Bold(p.get('name', p.get('preferredUsername'))),
            Label(f"@{p.get('preferredUsername')}@{p.get('id').split('/')[2]}", margin=Margin(top=Size.Relative.font(-0.5)))
        ], css={'float': 'left'}, margin=Margin(left=Size.pixel(10), top=Size.pixel(3)))
    ], margin=Margin(top=Size.pixel(10))),
    Container(
        childs=[x.get('content', '').replace('<script', '').replace('<style', '').replace('onload="', '')],
        margin=Margin(top=Size.Relative.font(5)),
    )
], x.get('id', '/404.py'))

ap_profile = lambda x: result([
    Container([
        '' if x.get('icon', {'url': None})['url'] is None else
        Container([
            Image(
                src=x.get('icon', {'url': None})['url'],
                alt='Profile Photo',
                height=Size.pixel(50),
                width=Size.pixel(50),
                border_radius=Size.percent(50)
            )
        ], css={'float': 'left'}),
        Container([
            Bold(x.get('name', x.get('preferredUsername'))),
            Label(f"@{x.get('preferredUsername')}@{x.get('id').split('/')[2]}", margin=Margin(top=Size.Relative.font(-0.5)))
        ], css={'float': 'left'}, margin=Margin(left=Size.pixel(10), top=Size.pixel(3)))
    ], margin=Margin(top=Size.pixel(10))),
    Container(
        childs=[x.get('summary', '').replace('<script', '').replace('<style', '').replace('onload="', '')],
        margin=Margin(top=Size.Relative.font(5)),
    )
], x.get('id', '/404.py'))


def x_post(i):
    # X is registered trademark of X Corp. HereUS Search is not affiliated with, endorsed by, or sponsored by X Corp.
    # Twitter is registered trademark of X Corp. HereUS Search is not affiliated with, endorsed by, or sponsored by X Corp.
    try:
        html = requests.get('https://publish.twitter.com/oembed?url='+i.url).json().get('html', None)
    except requests.exceptions.JSONDecodeError:
        return web_result(i)
    if html is None:
        web_result(i)
    return Container(
        selector='result',
        childs=[html],
        margin=Margin(bottom=Size.pixel(10)),
        width=Size.max_content,
        max_width=substract_style(Size.Viewport.width(100), Size.pixel(60)),
    )


def get(r: Request) -> Page:
    if r.query.get('q', None) is None:
        return redirect("/")
    r.query['q'] = r.query.get('q').replace('%40', '@').replace('+', ' ').replace('%3A', ':').replace('%23', '#')
    rl = r.user.search(r.query.get('q'))
    cl = []
    lk = []
    for i in rl:
        if i.url not in lk:
            lk.append(i.url)
            to_append = None
            if i.url.startswith('theprotocols://') or '://' not in i.url:
                x = i.url.removeprefix('theprotocols://')
                if '@' in x and len(x.split('@')) == 2:
                    to_append = user_result(User(x), x, Network(x.split('@')[1]))
            elif i.url.startswith('https://github.com/') and len(i.url.removesuffix('/').split('://')[1].split('/')) == 3:
                to_append = github_result(requests.get(
                    f"https://api.github.com/repos/{i.url.removesuffix('/').split('/')[-2]}/{i.url.removesuffix('/').split('/')[-1]}"
                ).json())
            elif (i.url.startswith('https://twitter.com/') or i.url.startswith('https://x.com/')) and 'status' in i.url:
                to_append = x_post(i)
            elif i.url.startswith('https://') and i.url.split('/')[3].startswith('@'):
                ap = requests.get(i.url, headers={'Accept': 'application/activity+json'})
                if ap.status_code == 200 and ap.content.decode().startswith('{'):
                    j = ap.json()
                    try:
                        if j.get('type') == 'Note':
                            to_append = ap_note(j, requests.get(j.get('attributedTo'), headers={'Accept': 'application/activity+json'}).json())
                        elif j.get('type') == 'Person':
                            to_append = ap_profile(j)
                        else:
                            to_append = f
                    except Exception as e:
                        pass
            if to_append is None:
                if i.url.split('/')[2] in news_websites:
                    to_append = article_result(i)
                else:
                    to_append = web_result(i)
            cl.append(to_append)
    return Page(
        title=f"{r.query.get('q')} - HereUS Search",
        selector=f'body_{r.user.id.settings.theme_color}',
        childs=[
            Container(
                position=Position.fixed(top=Size.pixel(10), right=Size.pixel(10)),
                onclick="window.location.href='/Profile.py'",
                childs=[
                    Button('small', innertext="Login")
                    if r.email.split('@')[0] == 'Guest' else
                    Image(
                        r.user.id.profile_photo,
                        alt="Your Account",
                        height=Size.pixel(50),
                        width=Size.pixel(50),
                        border_radius=Size.percent(50)
                    )
                ]
            ),
            Container(
                width=substract_style(Size.Viewport.width(100), Size.pixel(180)),
                max_width=Size.pixel(500),
                position=Position.fixed(
                    top=Size.pixel(10),
                    left=Size.pixel(10)
                ),
                childs=[
                    Form(
                        method='GET',
                        childs=[
                            Textbox(
                                selector="the_box",
                                name='q',
                                value=r.query.get('q'),
                                placeholder="Search Web...",
                                border_radius=Size.pixel(50),
                                width=Size.percent(100),
                                max_width=Size.percent(100),
                                height=Size.pixel(32),
                                font_size=Size.Relative.font(1),
                                padding=Padding(top=Size.pixel(6), left=Size.pixel(30)),
                                css={"border": "1px solid #808080A0"},
                            )
                        ]
                    )
                ]
            ),
            Root(
                margin=Margin(top=Size.pixel(70)),
                childs=cl
            ),
            Widget('script', src='https://platform.twitter.com/widgets.js', innertext='')
        ]
    )
