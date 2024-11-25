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

filterControl();

searchControl();
arrowControl();