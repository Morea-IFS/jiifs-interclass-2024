const element = (e) => document.querySelector(e);
const elements = (e) => document.querySelectorAll(e);

const informationNavManagment = () => {
    const ulNavInformationItems = elements('.information nav ul li');

    const onClickInItemInformation = (item) => {
        item.addEventListener('click', () => {
            ulNavInformationItems.forEach((item) => {
                item.classList.remove('active');
                element(`.${item.classList[0]}-content`).style.display = 'none';
            })
            item.classList.add('active');
            element(`.${item.classList[0]}-content`).style.display = 'flex';
        })
    }

    ulNavInformationItems.forEach((item => onClickInItemInformation(item)));

}

const menuMobileManagment = () => {
    const burguer = element('.icon-burguer');
    const nav = element('header nav ul');
    const elementsMobile = elements('.mobile')
    const close = element('.icon-close');

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

informationNavManagment();
menuMobileManagment();