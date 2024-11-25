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

const arrowControl = () => {
    const selectInputs = document.querySelectorAll('select')

    selectInputs.forEach(e => {
        const iconArrow = e.nextElementSibling

        e.addEventListener('click', () => {
            e.className.includes('active') ? e.classList.remove('active') : e.classList.add('active')

            if (e.className.includes('active')) {
                iconArrow.style.rotate = '180deg'
            } else {
                iconArrow.style.rotate = '0deg'
            }

        })
    })
}

const searchControl = () => {
    const searchInput = document.querySelector('.search-input')

    searchInput.addEventListener('keypress', () => {
        const searchValue = searchInput.value.toLowerCase()
        const searchResults = document.querySelectorAll('.games-container > .game-block')

        searchResults.forEach(e => {
            e.innerHTML.toLowerCase().includes(searchValue) ? e.style.display = 'block' : e.style.display = 'none'
        })
    })
}

const filterControl = () => {
    const filterInputs = document.querySelectorAll('.games-filter select');
    const filterResults = document.querySelectorAll('.games-container > .game-block');

    filterInputs.forEach(input => {
        input.addEventListener('change', () => {
            const filterValues = Array.from(filterInputs).map(select => select.value.toLowerCase());

            filterResults.forEach(element => {
                const matchesFilters = filterValues.every(value => {
                    return value === 'all' || element.textContent.toLowerCase().includes(value);
                });

                element.style.display = matchesFilters ? 'block' : 'none';
            });
        });
    });
};
const controlFunctionBar = () => {
    const itensNav = document.querySelectorAll('.menu-of-functions li');
    const gamesSection = document.querySelector('.games');
    const todayGamesSection = document.querySelector('.today-games');
    itensNav.forEach((item) => {
        item.addEventListener('click', () => {
            itensNav.forEach((item) => {
                item.classList.value.includes('activate') ? item.classList.remove('activate') : item.classList.add('activate')
            });
            if ( item.classList.value.includes('activate') && item.classList.value.includes('today') ) {
                gamesSection.style.display = 'none';
                todayGamesSection.style.display = 'block';
            }
            else {
                gamesSection.style.display = 'flex';
                todayGamesSection.style.display = 'none';
            }
        })
    });
};
controlFunctionBar();
filterControl();
menuMobileManagment();
searchControl();
arrowControl();