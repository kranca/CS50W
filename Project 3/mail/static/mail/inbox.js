document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-form').onsubmit = function(event) {
    event.preventDefault();
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    console.log('Submitting email: ', { recipients, subject, body });

    console.log(JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    }));

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
    .then(response => {
      const status = response.status;
      // const message = response.statusText;

      return response.json().then(data => ({
        status: status,
        response: data
      }));
    })
    .then(result => {
      console.log(result);
      if (result.status === 201) {
        load_mailbox('sent');
      } else {
        console.log('Something went wrong: ', result.response)
      }

    })
    .catch(error => {
      console.log('Error: ', error)
    });
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  if (mailbox === 'inbox') {
    fetch('emails/inbox')
    .then(response => response.json())
    .then(emails => {
      emails.forEach(email_item => {
        render_email(email_item);
      });
    })
  } else if (mailbox === 'sent') {
    fetch('emails/sent')
    .then(response => response.json())
    .then(emails => {
      emails.forEach(email_item => {
        render_email(email_item);
      });
    })
  } else if (mailbox === 'archive') {
    fetch('emails/archive')
    .then(response => response.json())
    .then(emails => {
      emails.forEach(email_item => {
        render_email(email_item);
      });
    })
  } else {
    console.log('Invalid mailbox');
  }
}

function render_email(email_item) {
  // Create a new card for each email item in a given inbox
  const card = document.createElement('div');
  card.className = 'email-card' + (email_item.read ? ' read' : '');
  card.innerHTML = `
    <div class="email-sender">${email_item.sender}</div>
    <div class="email-subject">${email_item.subject}</div>
    <div class="email-date">${email_item.timestamp}</div>
  `;

  // Click to view email detail and mark as read
  card.addEventListener('click', () => toggle_read(email_item.id));
  document.querySelector('#emails-view').appendChild(card);
}

function view_email(email_id) {
  fetch(`emails/${email_id}`)
  .then(response => response.json())
  .then(email_item => {
    const emailsView = document.querySelector('#emails-view');
    emailsView.innerHTML = '';
  
    // Create the main email container
    const emailContainer = document.createElement('div');
    emailContainer.className = 'email-detail-card';
  
    // Toolbar
    const toolbar = document.createElement('div');
    toolbar.className = 'email-toolbar';
    toolbar.innerHTML = `
      <button class="btn" id="reply-btn">Reply</button>
      <button class="btn" id="mark-unread-btn">Mark as ${email_item.read ? 'unread' : 'read'}</button>
      <button class="btn" id="archive-btn">${email_item.archived ? 'Unarchive' : 'Archive'}</button>
    `;
  
    // Header
    const header = document.createElement('div');
    header.className = 'email-header';
    header.innerHTML = `
      <div><strong>From:</strong> ${email_item.sender}</div>
      <div><strong>To:</strong> ${email_item.recipients.join(', ')}</div>
      <div><strong>Subject:</strong> ${email_item.subject}</div>
      <div><strong>Date:</strong> ${email_item.timestamp}</div>
    `;
  
    // Body
    const body = document.createElement('div');
    body.className = 'email-body';
    body.textContent = email_item.body;
  
    // Append everything
    emailContainer.appendChild(toolbar);
    emailContainer.appendChild(header);
    emailContainer.appendChild(body);
    emailsView.appendChild(emailContainer);
  
    // Button events
    // toolbar.querySelector('#reply-btn').addEventListener('click', () => reply_email(email));
    toolbar.querySelector('#mark-unread-btn').addEventListener('click', () => toggle_read(email_item.id, email_item.read));
    toolbar.querySelector('#archive-btn').addEventListener('click', () => toggle_archive(email_item.id, email_item.archived));
  });
}

function toggle_read(email_id, is_read) {
  fetch(`emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: !is_read
    })
  })
  .then(() => {
    view_email(email_id);
  });
}

function toggle_archive(email_id, is_archived) {
  fetch(`emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !is_archived
    })
  })
  .then(() => {
    load_mailbox('inbox');
  });
}