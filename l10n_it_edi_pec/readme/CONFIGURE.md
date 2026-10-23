**Italiano**

1. Configurare un server SMTP in uscita per la PEC:
   - Andare in *Impostazioni → Tecnico → Server di posta in uscita*
   - Creare un nuovo server con i parametri del provider PEC
   - Spuntare "E-invoice PEC server"
   - Inserire l'indirizzo email PEC mittente

2. Configurare un server di posta in ingresso per la PEC:
   - Andare in *Impostazioni → Tecnico → Server di posta in ingresso*
   - Creare un nuovo server IMAP o POP3 con i parametri del provider PEC
   - Spuntare "E-invoice PEC server"
   - Configurare i contatti da notificare in caso di errore

3. Abilitare il canale PEC per l'azienda:
   - Andare in *Impostazioni → Contabilità → Fatturazione elettronica*
   - Spuntare "Use PEC for e-invoicing"
   - Selezionare i server PEC in uscita e in ingresso
   - Inserire l'indirizzo PEC del SdI

4. Il parametro di sistema `fetchmail.pec.max.retry` (default: 5) controlla
   il numero massimo di errori consecutivi prima che il server di posta in
   ingresso venga disabilitato automaticamente. Modificare il valore in
   *Impostazioni → Tecnico → Parametri → Parametri di sistema* se necessario.

**English**

1. Configure an outgoing PEC SMTP server:
   - Go to *Settings → Technical → Outgoing Mail Servers*
   - Create a new server with your PEC provider parameters
   - Check "E-invoice PEC server"
   - Enter the PEC sender email address

2. Configure an incoming PEC mail server:
   - Go to *Settings → Technical → Incoming Mail Servers*
   - Create a new IMAP or POP3 server with your PEC provider parameters
   - Check "E-invoice PEC server"
   - Configure contacts to notify on errors

3. Enable PEC channel for the company:
   - Go to *Settings → Accounting → Italian Electronic Invoicing*
   - Check "Use PEC for e-invoicing"
   - Select the outgoing and incoming PEC servers
   - Enter the SdI PEC email address

4. The system parameter `fetchmail.pec.max.retry` (default: 5) controls
   the maximum number of consecutive errors before the incoming mail server
   is automatically disabled. Change its value in
   *Settings → Technical → Parameters → System Parameters* if needed.
