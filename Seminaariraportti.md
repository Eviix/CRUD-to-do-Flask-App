# Seminaariraportti - CRUD-to-do-Flask-App

## Tiivistelmä

Tarkoituksenani oli luoda to do lista -sovellus, jota voisi käyttää verkkoselaimessa. Halusin, että sovelluksen ominaisuuksiin kuuluisi lisäys, päivittäminen ja poistaminen. Käytin tähän tarkoitukseen Flask-kirjastoa Python-ohjelmointikielellä, ja sovelluksen tietokannan hallintaan käytin SQLite3-tietokantajärjestelmää. 

# 1.	Johdanto ja työskentelyvaiheet

Ohjelmistokehityksen teknologioita kurssin tarkoituksena oli oppia uusia taitoja, hyödyntäen työkaluja ja tekniikoita, joita ei ole aiemmin päässyt kokeilemaan. Tämä työ on tehty tutkiaksemme mahdollisuutta luoda toimiva to-do -sovellus käyttäen Flask-kirjastoa, SQLite3-tietokantaa ja hyödynsin myös bootstrap frameworkia, sillä halusin, että ulkoasu olisi selkeä ja responsiivinen. Työskentelyvaiheeni olivat seuraavat:

- Tutustuminen Flask-kirjastoon ja SQLite3-tietokantaan sekä niiden käyttöön.
- Flask-sovelluksen luominen ja sen liittäminen tietokantaan.
- Toteuttaa to-do -sovelluksen toiminnallisuuden - tehtävien lisääminen, muokkaaminen, ja poistaminen.
- Miettiä mitä muuta hyödyllistä voisin lisätä ja päädyin lisäämään ominaisuuden, jossa voi vaihtaa tehtävän tilaa (not started, in progress, completed)
- Bootstrapin lisääminen sovellukseen, jotta se olisi käyttäjäystävällisempi
- Lopuksi paransin vielä sovelluksen tyylejä

Minulla ei ole ollut aiempaa kokemusta web-sovelluksen luomista Python-kielellä hyödyntäen flask-kirjastoa, mutta olen käynyt Haaga-Helian tarjoaman Python kurssin. Jouduin kuitenkin ensiksi hakemaan tietoa Flask-kirjastosta, sillä se oli minulle kokonaan uusi asia. Oppaani olivat erityisesti Flask-dokumentaatio ja erilaiset YouTube tutoriaalit, joista sain hyvät ohjeet ja vinkit web-sovelluksen luomiseen. 

Kun olin perehtynyt Flask-kirjastoon tarpeeksi, aloin työstämään to do lista -sovellusta. Ensimmäiseksi asensin Pythonin ja flask-kirjaston joka tapahtuu seuraavasti:


```
pip install Flask
```
Tämän jälkeen loin app.py tiedoston ja lisäsin tarvittavatat importit:
```
from flask import Flask, request, redirect, url_for, render_template
```
Lähdin rakentamaan suoraan Flask-sovelluksen runkoa app.py tiedostoon ja alotin sen lisäämällä perustoiminnallisuutta, kuten reititystä eri sivuille ja HTTP-pyyntöjen käsittelyä. Eli ensiksi piti määrittää polut ja funktiot, joka tapahtui seuraavasti: **@app.route('/')** määrittää polun etusivulle, ja **@app.route('/todos', methods=['GET', 'POST'])** määrittää polun to do -listalle sekä sallii GET- ja POST-pyynnöt tälle polulle.

Myöhemmin lisäsin todo -listaan muita toiminnallisuuksia, jotka olivat lisäys, muokkaus ja poistaminen. Esimerkiksi, jos halusin lisätä muokkaus/päivitys ominaisuuden, niin se tapahtui seuraavasti:
```
//Tämä määrittää polun tehtävän muokkaamiseen
@app.route('/todos/<int:id>/edit', methods=['GET', 'POST'])
```
Tehtävän lisäys ja poistaminen toimii myös samalla logiikalla paitsi poistamiseen ei tarvitse GET-pyyntöä, sillä se ei ole luonteeltaan hakuoperaatio vaan siinä tehdään vain POST-pyyntö palvelimeen, jonka avulla se saa lähetettä tiedon palvelimeen.

Lopuksi, jotta HTML-sivustot näkyvät käyttäjälle, niin minun täytyi lisätä render_template -funktio, sillä ilman sitä sivut eivät näy.
```
// Esimerkki
return render_template('todos.html', todos=todos)
```

# 1.1 Liittäminen tietokantaan
```
// tietokannan lisääminen
import sqlite3
```
Tässä vaiheessa lähdin miettimään mitä tietokantaa käyttäisin ja päädyin käyttämään sqlite3, sillä se tuntui helpoimmalta käyttää. Lähdin luomaan SQLite-tietokantaa ja to-do lista -taulukkoa seuraavasti: 
```
// Tämä laitetaan @app.route('/') -funktion sisälle
conn = sqlite3.connect('todolist.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, task TEXT, status TEXT)')
c.close()
```
Jos käyttäjä tekee POST-pyynnön, uusi tehtävä lisätään tietokantaan seuraavasti:
```
// Tämä laitetaan @app.route('/todos') -funktion sisälle
// Tietokantaan yhdistämiseen vaaditaan myös: conn = sqlite3.connect('todolist.db')
//c = conn.cursor()
if request.method == 'POST':
    task = request.form['task']
    status = request.form['status']

    c.execute('INSERT INTO todos (task, status) VALUES (?, ?)', (task, status))
    conn.commit()
```
Jotta myös tehtävät näkyisi käyttäjille, niin se vaatii seuraavan:
```
c.execute('SELECT * FROM todos')
todos = c.fetchall()
```

Edit ja Delete toimivat samalla logiikalla, mutta tässä on lyhyesti laitettuna kaikki oleellinen mikä liittyy tietokantaan lisäämiseen.

# 2. Flask ja React eroavaisuudet

Minulla ei ole aiempaa kokemusta Flaskin käytöstä, mutta Reactia olen käyttänyt jo jonkin verran. Mitä huomasin tätä sovellusta tehdessä oli se, että Flaskin käyttö vaati huomattavasti vähemmän koodia verrattuna Reactiin. Halusin tehdä pienen vertauksen, että miltä samantyylinen sovellus näyttäisi Reactilla, joten tein siitä pienen version.

```
//Flask app.py
from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
   # Luodaan uusi SQLite-tietokanta ja luodaan to-do lista table
    conn = sqlite3.connect('todolist.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, task TEXT, status TEXT)')
    c.close()

    return redirect(url_for('todos'))

@app.route('/todos', methods=['GET', 'POST'])
def todos():
   # Yhdistetään SQLite-tietokantaan   
    conn = sqlite3.connect('todolist.db')
    c = conn.cursor()

    if request.method == 'POST':
    
        task = request.form['task']
        status = request.form['status']

        c.execute('INSERT INTO todos (task, status) VALUES (?, ?)', (task, status))
        conn.commit()

    c.execute('SELECT * FROM todos')
    todos = c.fetchall()

    c.close()
    return render_template('todos.html', todos=todos)
```
Tässä on React.js versio Flask sovelluksesta, mutta täytyy ottaa huomioon, että React sovelluksessa ei ole lisätty tietokantaa.

```
//React app.js
import React, { useState } from 'react';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState('');
  const [newStatus, setNewStatus] = useState('');

  const addTask = () => {
    setTasks([...tasks, { task: newTask, status: newStatus }]);
    
    setNewTask('');
    setNewStatus('');
  };

  return (
    <div className="App">
      <h1>To-Do List</h1>
      <ul>
        {tasks.map((task, index) => (
          <li key={index}>
            {task.task} - {task.status}
          </li>
        ))}
      </ul>
      <div>
        <input
          type="text"
          placeholder="New Task"
          value={newTask}
          onChange={e => setNewTask(e.target.value)}
        />
        <input
          type="text"
          placeholder="Status"
          value={newStatus}
          onChange={e => setNewStatus(e.target.value)}
        />
        <button onClick={addTask}>Add Task</button>
      </div>
    </div>
  );
}

export default App;
```

Flask ja React ovat molemmat eri tarkoituksiin tehty, mutta jos lähtisin tekemään jotain yksinkertaisia sovelluksia, kuten to do -lista, niin saattaisin silloin valita Flaskin. Flask tuntui ainakin itselleni yksinkertaisemmalta kirjastolta, kuin React.

## 3. Pohdinta
En ole ennen käyttänyt Flaskia, mutta sen ymmärtäminen oli yllättävän helppoa. Jos en olisi ennen käyttänyt mitään kehityskirjastoa, niin luultavasti alottaisin Flaskilla. Tietenkin pitää ottaa se huomioon, että Flask on yksinkertaisempi kirjasto, joka tuo myös rajotteita, jos aletaan rakentamaan jotain monimutkaisempia käyttöliittymiä. 

Positiivisena asiana oli se, että Flask vaati vähemmän riviä koodia verrattuna Reactiin. Uskon, että tulen käyttämään myös Flaskia jatkossa, enkä olisi varmaan ilman tätä kurssia käyttänyt sitä pitkään aikaan missään. Toisena mukavana yllätyksenä oli githubin tarjoama codespace, sillä se tuli kurssin aikana kaikille käytettäväksi. Uskon, että pilvessä pyörivät kehitysympäristöt tulevat olemaan tulevaisuudessa entistä suositumpia ja olen varma, että käytän sitä myös jatkossa. Pitää tietenkin mainita, että mikään ilmainen ei yleensä ole täysin ilmaista, sillä codespacessa on myös omat rajoitteet, eli voit kuukaudessa käyttää 60 tuntia ilmaiseksi ja sen jälkeen sen käytöstä pitää maksaa, jos haluaa jatkaa pilvessä koodaamista.

Tässä vielä muutama idea jatkokehitystä varten:
- Tehtäviin päivämäärän lisäys, eli voisi antaa jonkun deadlinen milloin joku tehtävä tulisi viimeistään suorittaa
- Tehtävien luokittelu eri kategorioihin (harrastukset, koulutyöt jne)
- Sivulle kirjautuminen 



## Lähteet

Flask’s documentation https://flask.palletsprojects.com/en/2.2.x/ Luettu 3.12.2022
Tech With Tim. Flask Tutorial #1- #4 https://www.youtube.com/watch?v=mqhxxeeTbu0&list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX Katsottu 4.12.2022
