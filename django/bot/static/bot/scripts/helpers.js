export async function handleRequest(headers_content, body_content) {
  try {
    const apiEndpont = "/api/get_response/";
    // const apiEndpont = "http://13.50.248.208/api/get_response/";
    // const apiEndpont = "http://localhost/api/get_response/";
    // const apiEndpont = "http://localhost:8000/api/get_response/"
    const res = await fetch(apiEndpont, {
      method: "POST",
      // credentials: "same-origin",
      body: body_content,
      headers: headers_content,
    });

    return await res.json();
  } catch (error) {
    console.log(error);
    throw error;
  }
}

export function getCsrfToken() {
  const csrfToken = document.cookie
    .split(";")
    .find((value) => value.includes("csrftoken"))
    .split("=")[1];

  return csrfToken;
}

const showPosition = (position) => {
  console.log(position);
  console.log(
    "Latitude: " +
      position.coords.latitude +
      " Longitude: " +
      position.coords.longitude
  );
};

const get_location = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    console.log("Geolocation is not supported by this browser.");
  }
};
