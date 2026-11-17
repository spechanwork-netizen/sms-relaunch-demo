# -*- coding: utf-8 -*-
"""Setzt die vom Kunden gelieferten Rechtstexte auf Impressum und Datenschutz.

  python3 -I rechtsseiten.py <website-ordner>

Der Text wird woertlich uebernommen; ergaenzt sind nur Struktur (Ueberschriften,
Absaetze, Listen) und klickbare Telefon- und E-Mail-Verweise.
Mehrfach ausfuehrbar.
"""
import sys, os, re

SITE = sys.argv[1]
TEL = '<a href="tel:+499103918490">+49 9103 91849 0</a>'
MAIL = '<a href="mailto:info@sms.gmbh">info@sms.gmbh</a>'


def h2(t):
    return f'<h2 class="t-title-lg">{t}</h2>'


def h3(t):
    return f'<h3 class="t-title-md">{t}</h3>'


def p(t):
    return f'<p class="t-body-md">{t}</p>'


def ul(punkte):
    return '<ul class="t-body-md">' + "".join(f"<li>{x}</li>" for x in punkte) + "</ul>"


# ---------------------------------------------------------------- Impressum
IMPRESSUM = [
    h2("Angaben gemäß § 5 DDG"),
    p("sms engineering GmbH<br>Seckendorfer Str. 6<br>90556 Cadolzburg"),
    p("Handelsregister: HRB 8473<br>Registergericht: Amtsgericht Fürth / Bay."),
    h2("Vertreten durch"),
    p("Christian Schmidt, Robert Maas"),
    h2("Kontakt"),
    p(f"Telefon: {TEL}<br>E-Mail: {MAIL}"),
    h2("Umsatzsteuer-ID"),
    p("Umsatzsteuer-Identifikationsnummer gemäß § 27 a Umsatzsteuergesetz:<br>DE 813.180.717"),
    h2("Streitschlichtung"),
    p("Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer "
      "Verbraucherschlichtungsstelle teilzunehmen."),
    h2("Haftung für Inhalte"),
    p("Als Diensteanbieter sind wir nach den allgemeinen Gesetzen sowie den Vorschriften der "
      "Verordnung (EU) 2022/2065 (Digital Services Act) für eigene Inhalte auf diesen Seiten "
      "verantwortlich. Wir sind jedoch nicht verpflichtet, übermittelte oder gespeicherte fremde "
      "Informationen zu überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige "
      "Tätigkeit hinweisen."),
    p("Verpflichtungen zur Entfernung oder Sperrung der Nutzung von Informationen nach den "
      "allgemeinen Gesetzen bleiben hiervon unberührt. Eine diesbezügliche Haftung ist jedoch erst "
      "ab dem Zeitpunkt der Kenntnis einer konkreten Rechtsverletzung möglich. Bei Bekanntwerden "
      "von entsprechenden Rechtsverletzungen werden wir diese Inhalte umgehend entfernen."),
    h2("Haftung für Links"),
    p("Unser Angebot enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen "
      "Einfluss haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen. "
      "Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der "
      "Seiten verantwortlich. Die verlinkten Seiten wurden zum Zeitpunkt der Verlinkung auf "
      "mögliche Rechtsverstöße überprüft. Rechtswidrige Inhalte waren zum Zeitpunkt der "
      "Verlinkung nicht erkennbar."),
    p("Eine permanente inhaltliche Kontrolle der verlinkten Seiten ist jedoch ohne konkrete "
      "Anhaltspunkte einer Rechtsverletzung nicht zumutbar. Bei Bekanntwerden von "
      "Rechtsverletzungen werden wir derartige Links umgehend entfernen."),
    h2("Urheberrecht"),
    p("Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen "
      "dem deutschen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art der "
      "Verwertung außerhalb der Grenzen des Urheberrechtes bedürfen der schriftlichen Zustimmung "
      "des jeweiligen Autors bzw. Erstellers. Downloads und Kopien dieser Seite sind nur für den "
      "privaten, nicht kommerziellen Gebrauch gestattet."),
    p("Soweit die Inhalte auf dieser Seite nicht vom Betreiber erstellt wurden, werden die "
      "Urheberrechte Dritter beachtet. Insbesondere werden Inhalte Dritter als solche "
      "gekennzeichnet. Sollten Sie trotzdem auf eine Urheberrechtsverletzung aufmerksam werden, "
      "bitten wir um einen entsprechenden Hinweis. Bei Bekanntwerden von Rechtsverletzungen werden "
      "wir derartige Inhalte umgehend entfernen."),
]

# ------------------------------------------------------------- Datenschutz
GROSS = ('<p class="t-body-md" style="font-size: 15px; letter-spacing: .01em">%s</p>')

DATENSCHUTZ = [
    h2("1. Datenschutz auf einen Blick"),
    h3("Allgemeine Hinweise"),
    p("Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren "
      "personenbezogenen Daten passiert, wenn Sie diese Website besuchen. Personenbezogene Daten "
      "sind alle Daten, mit denen Sie persönlich identifiziert werden können. Ausführliche "
      "Informationen zum Thema Datenschutz entnehmen Sie unserer unter diesem Text aufgeführten "
      "Datenschutzerklärung."),
    h3("Datenerfassung auf dieser Website"),
    p("<strong>Wer ist verantwortlich für die Datenerfassung auf dieser Website?</strong><br>"
      "Die Datenverarbeitung auf dieser Website erfolgt durch den Websitebetreiber. Dessen "
      'Kontaktdaten können Sie dem <a href="impressum.html">Impressum</a> dieser Website entnehmen.'),
    p("<strong>Wie erfassen wir Ihre Daten?</strong><br>"
      "Ihre Daten werden zum einen dadurch erhoben, dass Sie uns diese mitteilen. Hierbei kann es "
      "sich z. B. um Daten handeln, die Sie uns per E-Mail oder Telefon mitteilen."),
    p("Andere Daten werden automatisch beim Besuch der Website durch unsere IT-Systeme erfasst. "
      "Das sind vor allem technische Daten (z. B. Internetbrowser, Betriebssystem oder Uhrzeit des "
      "Seitenaufrufs). Die Erfassung dieser Daten erfolgt automatisch, sobald Sie diese Website "
      "betreten."),
    p("<strong>Wofür nutzen wir Ihre Daten?</strong><br>"
      "Die Daten werden erhoben, um eine fehlerfreie Bereitstellung der Website zu gewährleisten "
      "und um Ihre Anfragen zu bearbeiten."),
    p("<strong>Welche Rechte haben Sie bezüglich Ihrer Daten?</strong><br>"
      "Sie haben jederzeit das Recht unentgeltlich Auskunft über Herkunft, Empfänger und Zweck "
      "Ihrer gespeicherten personenbezogenen Daten zu erhalten. Sie haben außerdem ein Recht, die "
      "Berichtigung oder Löschung dieser Daten zu verlangen. Hierzu sowie zu weiteren Fragen zum "
      "Thema Datenschutz können Sie sich jederzeit unter der im Impressum angegebenen Adresse an "
      "uns wenden. Des Weiteren steht Ihnen ein Beschwerderecht bei der zuständigen "
      "Aufsichtsbehörde zu."),
    p("Außerdem haben Sie das Recht, unter bestimmten Umständen die Einschränkung der Verarbeitung "
      "Ihrer personenbezogenen Daten zu verlangen. Details hierzu entnehmen Sie der "
      "Datenschutzerklärung unter „Recht auf Einschränkung der Verarbeitung“."),
    h3("Analyse-Tools und Tools von Drittanbietern"),
    p("Diese Website verwendet keine Analyse- oder Tracking-Tools. Es werden keine Inhalte von "
      "Drittanbietern (z. B. Schriftarten, Karten oder Videos) eingebunden."),

    h2("2. Hosting"),
    h3("Externes Hosting"),
    p("Wir hosten die Inhalte unserer Website bei der IONOS SE, Elgendorfer Str. 57, 56410 "
      "Montabaur (nachfolgend IONOS). Wenn Sie unsere Website besuchen, erfasst IONOS verschiedene "
      "Logfiles inklusive Ihrer IP-Adresse."),
    p("Personenbezogenen Daten, die auf dieser Website erfasst werden, werden auf den Servern des "
      "Hosters gespeichert. Hierbei kann es sich v. a. um IP-Adressen, Kontaktanfragen, Meta- und "
      "Kommunikationsdaten, Vertragsdaten, Kontaktdaten, Namen, Webseitenzugriffe und sonstige "
      "Daten, die über eine Website generiert werden, handeln."),
    p("Der Einsatz des Hosters erfolgt zum Zwecke der Vertragserfüllung gegenüber unseren "
      "potenziellen und bestehenden Kunden (Art. 6 Abs. 1 lit. b DSGVO) und im Interesse einer "
      "sicheren, schnellen und effizienten Bereitstellung unseres Online-Angebots durch einen "
      "professionellen Anbieter (Art. 6 Abs. 1 lit. f DSGVO)."),
    p("Unser Hoster wird Ihre Daten nur insoweit verarbeiten, wie dies zur Erfüllung seiner "
      "Leistungspflichten erforderlich ist und unsere Weisungen in Bezug auf diese Daten befolgen."),
    h3("Abschluss eines Vertrages über Auftragsverarbeitung"),
    p("Um die datenschutzkonforme Verarbeitung zu gewährleisten, haben wir einen Vertrag über "
      "Auftragsverarbeitung mit IONOS geschlossen."),

    h2("3. Allgemeine Hinweise und Pflichtinformationen"),
    h3("Datenschutz"),
    p("Die Betreiber dieser Seiten nehmen den Schutz Ihrer persönlichen Daten sehr ernst. Wir "
      "behandeln Ihre personenbezogenen Daten vertraulich und entsprechend der gesetzlichen "
      "Datenschutzvorschriften sowie dieser Datenschutzerklärung."),
    p("Wenn Sie diese Website benutzen, werden verschiedene personenbezogene Daten erhoben. "
      "Personenbezogene Daten sind Daten, mit denen Sie persönlich identifiziert werden können. "
      "Die vorliegende Datenschutzerklärung erläutert, welche Daten wir erheben und wofür wir sie "
      "nutzen. Sie erläutert auch, wie und zu welchem Zweck das geschieht."),
    p("Wir weisen darauf hin, dass die Datenübertragung im Internet (z. B. bei der Kommunikation "
      "per E-Mail) Sicherheitslücken aufweisen kann. Ein lückenloser Schutz der Daten vor dem "
      "Zugriff durch Dritte ist nicht möglich."),
    h3("Hinweis zur verantwortlichen Stelle"),
    p("Die verantwortliche Stelle für die Datenverarbeitung auf dieser Website ist:"),
    p(f"sms engineering GmbH<br>Seckendorfer Straße 6<br>90556 Cadolzburg<br>"
      f"Telefon: {TEL}<br>E-Mail: {MAIL}"),
    p("Verantwortliche Stelle ist die natürliche oder juristische Person, die allein oder "
      "gemeinsam mit anderen über die Zwecke und Mittel der Verarbeitung von personenbezogenen "
      "Daten (z. B. Namen, E-Mail-Adressen o. Ä.) entscheidet."),
    h3("Kontaktdaten des Datenschutzbeauftragten"),
    p("Unseren Datenschutzbeauftragten:"),
    p("Herrn Rechtsanwalt Christian Krösch<br>SLK Compliance Services GmbH<br>"
      "Königsbrücker Straße 76<br>01099 Dresden"),
    p('erreichen Sie per Telefon: <a href="tel:+4935189676360">0351 89676360</a> oder E-Mail: '
      '<a href="mailto:datenschutz@slk-compliance.de">datenschutz@slk-compliance.de</a>'),
    h3("Widerruf Ihrer Einwilligung zur Datenverarbeitung"),
    p("Viele Datenverarbeitungsvorgänge sind nur mit Ihrer ausdrücklichen Einwilligung möglich. "
      "Sie können eine bereits erteilte Einwilligung jederzeit widerrufen. Dazu reicht eine "
      "formlose Mitteilung per E-Mail an uns. Die Rechtmäßigkeit der bis zum Widerruf erfolgten "
      "Datenverarbeitung bleibt vom Widerruf unberührt."),
    h3("Widerspruchsrecht gegen die Datenerhebung in besonderen Fällen sowie gegen Direktwerbung "
       "(Art. 21 DSGVO)"),
    GROSS % ("WENN DIE DATENVERARBEITUNG AUF GRUNDLAGE VON ART. 6 ABS. 1 LIT. E ODER F DSGVO "
             "ERFOLGT, HABEN SIE JEDERZEIT DAS RECHT, AUS GRÜNDEN, DIE SICH AUS IHRER BESONDEREN "
             "SITUATION ERGEBEN, GEGEN DIE VERARBEITUNG IHRER PERSONENBEZOGENEN DATEN WIDERSPRUCH "
             "EINZULEGEN; DIES GILT AUCH FÜR EIN AUF DIESE BESTIMMUNGEN GESTÜTZTES PROFILING. DIE "
             "JEWEILIGE RECHTSGRUNDLAGE, AUF DENEN EINE VERARBEITUNG BERUHT, ENTNEHMEN SIE DIESER "
             "DATENSCHUTZERKLÄRUNG. WENN SIE WIDERSPRUCH EINLEGEN, WERDEN WIR IHRE BETROFFENEN "
             "PERSONENBEZOGENEN DATEN NICHT MEHR VERARBEITEN, ES SEI DENN, WIR KÖNNEN ZWINGENDE "
             "SCHUTZWÜRDIGE GRÜNDE FÜR DIE VERARBEITUNG NACHWEISEN, DIE IHRE INTERESSEN, RECHTE "
             "UND FREIHEITEN ÜBERWIEGEN ODER DIE VERARBEITUNG DIENT DER GELTENDMACHUNG, AUSÜBUNG "
             "ODER VERTEIDIGUNG VON RECHTSANSPRÜCHEN (WIDERSPRUCH NACH ART. 21 ABS. 1 DSGVO)."),
    GROSS % ("WERDEN IHRE PERSONENBEZOGENEN DATEN VERARBEITET, UM DIREKTWERBUNG ZU BETREIBEN, SO "
             "HABEN SIE DAS RECHT, JEDERZEIT WIDERSPRUCH GEGEN DIE VERARBEITUNG SIE BETREFFENDER "
             "PERSONENBEZOGENER DATEN ZUM ZWECKE DERARTIGER WERBUNG EINZULEGEN; DIES GILT AUCH FÜR "
             "DAS PROFILING, SOWEIT ES MIT SOLCHER DIREKTWERBUNG IN VERBINDUNG STEHT. WENN SIE "
             "WIDERSPRECHEN, WERDEN IHRE PERSONENBEZOGENEN DATEN ANSCHLIESSEND NICHT MEHR ZUM "
             "ZWECKE DER DIREKTWERBUNG VERWENDET (WIDERSPRUCH NACH ART. 21 ABS. 2 DSGVO)."),
    h3("Beschwerderecht bei der zuständigen Aufsichtsbehörde"),
    p("Im Falle von Verstößen gegen die DSGVO steht den Betroffenen ein Beschwerderecht bei einer "
      "Aufsichtsbehörde, insbesondere in dem Mitgliedstaat ihres gewöhnlichen Aufenthalts, ihres "
      "Arbeitsplatzes oder des Orts des mutmaßlichen Verstoßes zu. Das Beschwerderecht besteht "
      "unbeschadet anderweitiger verwaltungsrechtlicher oder gerichtlicher Rechtsbehelfe."),
    h3("Recht auf Datenübertragbarkeit"),
    p("Sie haben das Recht, Daten, die wir auf Grundlage Ihrer Einwilligung oder in Erfüllung "
      "eines Vertrags automatisiert verarbeiten, an sich oder an einen Dritten in einem gängigen, "
      "maschinenlesbaren Format aushändigen zu lassen. Sofern Sie die direkte Übertragung der "
      "Daten an einen anderen Verantwortlichen verlangen, erfolgt dies nur, soweit es technisch "
      "machbar ist."),
    h3("Auskunft, Löschung und Berichtigung"),
    p("Sie haben im Rahmen der geltenden gesetzlichen Bestimmungen jederzeit das Recht auf "
      "unentgeltliche Auskunft über Ihre gespeicherten personenbezogenen Daten, deren Herkunft und "
      "Empfänger und den Zweck der Datenverarbeitung und ggf. ein Recht auf Berichtigung oder "
      "Löschung dieser Daten. Hierzu sowie zu weiteren Fragen zum Thema personenbezogene Daten "
      "können Sie sich jederzeit unter der im Impressum angegebenen Adresse an uns wenden."),
    h3("Recht auf Einschränkung der Verarbeitung"),
    p("Sie haben das Recht, die Einschränkung der Verarbeitung Ihrer personenbezogenen Daten zu "
      "verlangen. Hierzu können Sie sich jederzeit unter der im Impressum angegebenen Adresse an "
      "uns wenden. Das Recht auf Einschränkung der Verarbeitung besteht in folgenden Fällen:"),
    ul(["Wenn Sie die Richtigkeit Ihrer bei uns gespeicherten personenbezogenen Daten bestreiten, "
        "benötigen wir in der Regel Zeit, um dies zu überprüfen. Für die Dauer der Prüfung haben "
        "Sie das Recht, die Einschränkung der Verarbeitung Ihrer personenbezogenen Daten zu "
        "verlangen.",
        "Wenn die Verarbeitung Ihrer personenbezogenen Daten unrechtmäßig geschah/geschieht, "
        "können Sie statt der Löschung die Einschränkung der Datenverarbeitung verlangen.",
        "Wenn wir Ihre personenbezogenen Daten nicht mehr benötigen, Sie sie jedoch zur Ausübung, "
        "Verteidigung oder Geltendmachung von Rechtsansprüchen benötigen, haben Sie das Recht, "
        "statt der Löschung die Einschränkung der Verarbeitung Ihrer personenbezogenen Daten zu "
        "verlangen.",
        "Wenn Sie einen Widerspruch nach Art. 21 Abs. 1 DSGVO eingelegt haben, muss eine Abwägung "
        "zwischen Ihren und unseren Interessen vorgenommen werden. Solange noch nicht feststeht, "
        "wessen Interessen überwiegen, haben Sie das Recht, die Einschränkung der Verarbeitung "
        "Ihrer personenbezogenen Daten zu verlangen."]),
    p("Wenn Sie die Verarbeitung Ihrer personenbezogenen Daten eingeschränkt haben, dürfen diese "
      "Daten – von ihrer Speicherung abgesehen – nur mit Ihrer Einwilligung oder zur "
      "Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen oder zum Schutz der Rechte "
      "einer anderen natürlichen oder juristischen Person oder aus Gründen eines wichtigen "
      "öffentlichen Interesses der Europäischen Union oder eines Mitgliedstaats verarbeitet werden."),
    h3("Widerspruch gegen Werbe-E-Mails"),
    p("Der Nutzung von im Rahmen der Impressumspflicht veröffentlichten Kontaktdaten zur "
      "Übersendung von nicht ausdrücklich angeforderter Werbung und Informationsmaterialien wird "
      "hiermit widersprochen. Die Betreiber der Seiten behalten sich ausdrücklich rechtliche "
      "Schritte im Falle der unverlangten Zusendung von Werbeinformationen, etwa durch "
      "Spam-E-Mails, vor."),

    h2("4. Datenerfassung auf dieser Website"),
    h3("Cookies"),
    p("Die Internetseiten verwenden teilweise so genannte Cookies. Cookies richten auf Ihrem "
      "Rechner keinen Schaden an und enthalten keine Viren. Cookies dienen dazu, unser Angebot "
      "nutzerfreundlicher, effektiver und sicherer zu machen. Cookies sind kleine Textdateien, die "
      "auf Ihrem Rechner abgelegt werden und die Ihr Browser speichert."),
    p("Die meisten der von uns verwendeten Cookies sind so genannte „Session-Cookies“. Sie werden "
      "nach Ende Ihres Besuchs automatisch gelöscht. Andere Cookies bleiben auf Ihrem Endgerät "
      "gespeichert bis Sie diese löschen. Diese Cookies ermöglichen es uns, Ihren Browser beim "
      "nächsten Besuch wiederzuerkennen."),
    p("Sie können Ihren Browser so einstellen, dass Sie über das Setzen von Cookies informiert "
      "werden und Cookies nur im Einzelfall erlauben, die Annahme von Cookies für bestimmte Fälle "
      "oder generell ausschließen sowie das automatische Löschen der Cookies beim Schließen des "
      "Browsers aktivieren. Bei der Deaktivierung von Cookies kann die Funktionalität dieser "
      "Website eingeschränkt sein."),
    p("Cookies, die zur Durchführung des elektronischen Kommunikationsvorgangs oder zur "
      "Bereitstellung bestimmter, von Ihnen erwünschter Funktionen (z. B. Warenkorbfunktion) "
      "erforderlich sind, werden auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO gespeichert. Der "
      "Websitebetreiber hat ein berechtigtes Interesse an der Speicherung von Cookies zur "
      "technisch fehlerfreien und optimierten Bereitstellung seiner Dienste. Sofern eine "
      "entsprechende Einwilligung abgefragt wurde (z. B. eine Einwilligung zur Speicherung von "
      "Cookies), erfolgt die Verarbeitung ausschließlich auf Grundlage von Art. 6 Abs. 1 lit. a "
      "DSGVO; die Einwilligung ist jederzeit widerrufbar."),
    p("Soweit andere Cookies (z. B. Cookies zur Analyse Ihres Surfverhaltens) gespeichert werden, "
      "werden diese in dieser Datenschutzerklärung gesondert behandelt."),
    h3("Server-Log-Dateien"),
    p("Der Provider der Seiten erhebt und speichert automatisch Informationen in so genannten "
      "Server-Log-Dateien, die Ihr Browser automatisch an uns übermittelt. Dies sind:"),
    ul(["Browsertyp und Browserversion", "verwendetes Betriebssystem", "Referrer URL",
        "Hostname des zugreifenden Rechners", "Uhrzeit der Serveranfrage", "IP-Adresse"]),
    p("Eine Zusammenführung dieser Daten mit anderen Datenquellen wird nicht vorgenommen."),
    p("Die Erfassung dieser Daten erfolgt auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO. Der "
      "Websitebetreiber hat ein berechtigtes Interesse an der technisch fehlerfreien Darstellung "
      "und der Optimierung seiner Website – hierzu müssen die Server-Log-Files erfasst werden."),
    h3("Anfrage per E-Mail, Telefon oder Telefax"),
    p("Wenn Sie uns per E-Mail, Telefon oder Telefax kontaktieren, wird Ihre Anfrage inklusive "
      "aller daraus hervorgehenden personenbezogenen Daten (Name, Anfrage) zum Zwecke der "
      "Bearbeitung Ihres Anliegens bei uns gespeichert und verarbeitet. Diese Daten geben wir "
      "nicht ohne Ihre Einwilligung weiter."),
    p("Die Verarbeitung dieser Daten erfolgt auf Grundlage von Art. 6 Abs. 1 lit. b DSGVO, sofern "
      "Ihre Anfrage mit der Erfüllung eines Vertrags zusammenhängt oder zur Durchführung "
      "vorvertraglicher Maßnahmen erforderlich ist. In allen übrigen Fällen beruht die "
      "Verarbeitung auf Ihrer Einwilligung (Art. 6 Abs. 1 lit. a DSGVO) und/oder auf unseren "
      "berechtigten Interessen (Art. 6 Abs. 1 lit. f DSGVO), da wir ein berechtigtes Interesse an "
      "der effektiven Bearbeitung der an uns gerichteten Anfragen haben."),
    p("Die von Ihnen an uns per Kontaktanfragen übersandten Daten verbleiben bei uns, bis Sie uns "
      "zur Löschung auffordern, Ihre Einwilligung zur Speicherung widerrufen oder der Zweck für "
      "die Datenspeicherung entfällt (z. B. nach abgeschlossener Bearbeitung Ihres Anliegens). "
      "Zwingende gesetzliche Bestimmungen – insbesondere gesetzliche Aufbewahrungsfristen – "
      "bleiben unberührt."),
]


def setze(datei, teile, titel):
    pfad = os.path.join(SITE, datei)
    s = open(pfad, encoding="utf-8").read()
    a = s.index('<div class="legal__inner">') + len('<div class="legal__inner">')
    b = s.index("</div>", a)
    inhalt = "\n      " + "\n      ".join(teile) + "\n    "
    s = s[:a] + inhalt + s[b:]
    # Untertitel im Bildkopf: die Seite traegt ihren Namen bereits als H1
    s = re.sub(r"<title>.*?</title>", f"<title>{titel} | sms engineering GmbH</title>", s, count=1)
    open(pfad, "w", encoding="utf-8").write(s)
    print(f"{datei}: {len(teile)} Bloecke gesetzt")


setze("impressum.html", IMPRESSUM, "Impressum")
setze("datenschutz.html", DATENSCHUTZ, "Datenschutzerklärung")
