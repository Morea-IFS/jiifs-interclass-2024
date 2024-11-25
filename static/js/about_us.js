const menuMobileManagment = () => {
    const burguer = document.querySelector('.icon-burguer');
    const nav = document.querySelector('header nav ul');
    const elementsMobile = document.querySelectorAll('.mobile')
    const close = document.querySelector('.icon-close');

    const onBurguerClick = () => {
        nav.style.display = 'flex';
        elementsMobile.forEach((item) => {
            item.style.display = 'flex';
        })
    };

    const onCloseClick = () => {
        nav.style.display = 'none';
        elementsMobile.forEach((item) => {
            item.style.display = 'none';
        })
    };

    burguer.addEventListener('click', onBurguerClick);
    close.addEventListener('click', onCloseClick);
}
menuMobileManagment();

const Data = [];
const advisorsContainer = document.querySelector('.advisors .members');
const membersContainer = document.querySelector('.active-members .members');

fetch('static/js/members.json')
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch data: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        data.forEach(member => {
            Data.push(member); // Preenche o array com os membros
        });
        renderMembers(); // Chama a função após os dados serem carregados
    })
    .catch(error => {
        console.error('Error fetching members:', error);
    });

    const renderMembers = () => {
        Data.forEach(member => {
            let memberDiv = document.createElement('div');
            memberDiv.className = "member";
            memberDiv.innerHTML = `
                            <div class="photo-person">
                                <img src="static/${member.image}" alt="Foto do Membro"/>
                            </div>
                            <div class="content-of-person">
                                <h3>${member.name}</h3>
                                <p>${member.description}</p>
                                <a class="link-morea-or-lattes" href="${member.lattes}" target="_blank">Currículo Lattes</a>
                                <div class="socia-media">
                                    <a href="${member.instagram}" target="_blank"><img src="static/images/icon-instagram-colorful.svg" alt="Instagram" aria-hidden="true"></a>
                                    <a href="${member.github}" target="_blank"><img src="static/images/icon-github.svg" alt="Github" aria-hidden="true"></a>
                                </div>
                            </div>
            `;
            member.type_member === 'advisor' ? advisorsContainer.appendChild(memberDiv) : membersContainer.appendChild(memberDiv);
        });
    };