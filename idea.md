# ZeroCalendar

FRONTEND

Interfaccia semplicissima, c'è il mese corrente con un box con scritta una parentesi col numero di impegni, proprio come un vero calendario.
In alto posso scorrere di anno, se clicco sull'anno si apre un menu a tendina scorrevole, e idem per il mese.



DATABASE:

users(id, name, session_cookie, created_at)

day_events(id, user_id, created_at, when, description) 
    user_id is a FK to users(id)


DB INTERACTION

Un utente può darsi un nome, non è importante creare una vera utenza.  
Al login, viene assegnato un session_cookie permanente, perché sinceramente per un utilizzo casalingo è più che sufficiente,
nessuno vuole cambiare utenza né nome perché l'unico scopo dell'utenza è di avere il tuo nome accanto all'impegno, why not?
