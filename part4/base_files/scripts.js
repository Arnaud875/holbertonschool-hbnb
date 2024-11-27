const API_ENDPOINT = "http://127.0.0.1:5000/api/v1";

function getCookie(cookie_name) {
    let token = null;

    document.cookie.split(';').forEach(cookie => {
        const [name, value] = cookie.split('=');

        if (name.trim() == cookie_name) {
            token = value;
            return value;
        }
    });

    return token;
}

async function isTokenValid(token) {
    const data = await (await fetch(`${API_ENDPOINT}/auth/protected`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })).json();

    return data.message || false;
}

async function fetchPlaces() {
    return (await (await fetch(`${API_ENDPOINT}/places/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })).json());
}

async function fetchPlaceDetails(token, place_id) {
    return (await (await fetch(`${API_ENDPOINT}/places/${place_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    })).json());
}

async function fetchUserInfo(user_id) {
    return (await (await fetch(`${API_ENDPOINT}/users/${user_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })).json());
}

function loginRoute() {
    const form = document.querySelector('form');
    const result_p = document.getElementById('login-result')

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        const response = await fetch(`${API_ENDPOINT}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (data.error) {
            result_p.textContent = data.error;
            result_p.style.color = 'red';
        } else {
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
        }
    });
}

async function indexRoute() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token || !(await isTokenValid(token)))
        return;

    loginLink.style.display = 'none';

    const fetch_place_by_filter = async (filter_name) => {
        const places = await fetchPlaces();
        const places_container = document.getElementById("places-container");
        const fix_filter = filter_name.replace("$", "");

        const create_card = (name, price, id) => {
            return `<div class="place-card">
                    <h2>${name}</h2>
                    <p>Price per Night: $${price}</p>
                    <button class="details-button" data-id="${id}">View Details</button>
                </div>`
        }

        places_container.innerHTML = "";
        places.forEach(async place => {
            const price = (await fetchPlaceDetails(token, place.id)).price

            if (filter_name != "all" && price > Number(fix_filter))
                return;

            const card = create_card(place.title, String(price), place.id);
            places_container.innerHTML += card;
        });
    }

    document.getElementById("places-container").addEventListener("click", async (e) => {
        if (e.target.classList.contains("details-button")) {
            const placeId = e.target.dataset.id;
            window.location.href = `place.html?id=${placeId}`;
        }
    });

    const price_filter = document.getElementById("price-filter");
    price_filter.addEventListener("change", () => fetch_place_by_filter(price_filter.value));
    fetch_place_by_filter("all");
}

async function placeRoute() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token || !(await isTokenValid(token)))
        return;

    loginLink.style.display = 'none';

    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    fetchPlaceDetails(token, placeId).then(async data => {
        if (data.error)
            return;

        const host_name = data.owner.first_name + " " + data.owner.last_name;

        document.getElementById('place-user').innerHTML = `<strong>Host:</strong> ${host_name}`;
        document.getElementById('place-title').textContent = data.title;
        document.getElementById('place-description').innerHTML = `<strong>Description:</strong> ${data.description}`;
        document.getElementById('place-price').innerHTML = `<strong>Price per night:</strong> $${data.price}`;

        const amenities = document.getElementById('place-amenities');
        amenities.innerHTML = "";

        data.amenities.forEach(amenity => amenities.innerHTML += `<span class="amenity">${amenity.name}</span>`);

        const reviews = document.getElementById("reviews-section");
        reviews.innerHTML = "<h2>Reviews</h2>";

        const reviewsPromises = data.reviews.map(async review => {
            const user = await fetchUserInfo(review.user_id);
            const user_full_name = user.first_name + " " + user.last_name;
            let rating_str = "";

            for (let i = 0; i < 5; i++) {
            if (i >= review.rating)
                rating_str += "☆";
            else
                rating_str += "★";
            }

            reviews.innerHTML += `<div class="review-card">
            <p class="review-author">${user_full_name}</p>
            <p>${review.text}</p>
            <div class="rating">${rating_str}</div>
            </div>`;
        });

        await Promise.all(reviewsPromises);

        reviews.innerHTML += `<a href="add_review.html?id=${placeId}" class="details-button">Add Review</a>`;
    });
}

async function addReviewRoute() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token || !(await isTokenValid(token)))
        return;

    loginLink.style.display = 'none';

    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    const form = document.querySelector('form');
    const result_p = document.getElementById('review-result');

    // ¯\_(ツ)_/¯
    let user_id = (await (await fetch(`${API_ENDPOINT}/auth/protected`, {method: 'GET', headers: { "Authorization": `Bearer ${token}` }})).json())["message"];
    user_id = user_id.replace("Hello, user ", "");

    const placeDetails = await fetchPlaceDetails(token, placeId);
    if (placeDetails.error)
        return;

    document.getElementById('place-title').textContent = `Reviewing: ${placeDetails.title}`;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const rating = document.getElementById('rating').value;
        const text = document.getElementById('review').value;


        const response = await fetch(`${API_ENDPOINT}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                "text": text,
                "rating": Number(rating),
                "user_id": user_id,
                "place_id": placeId
            })
        });

        const data = await response.json();
        if (data.error) {
            result_p.textContent = data.error;
            result_p.style.color = 'red';
        } else {
            alert('Review submitted successfully!');
            window.location.href = `place.html?id=${placeId}`;
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    switch(window.location.pathname.split('/').pop()) {
        case "login.html":
            loginRoute();
            break;
        case "index.html":
            indexRoute();
            break;
        case "place.html":
            placeRoute();
            break;
        case "add_review.html":
            addReviewRoute();
            break;
        default:
            break;
    }
});