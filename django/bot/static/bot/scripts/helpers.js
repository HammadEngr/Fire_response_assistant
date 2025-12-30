export async function handleRequest(headers_content, body_content) {
  try {
    const res = await fetch("http://localhost:8000/api/get_response/", {
      method: "POST",
      credentials: "same-origin",
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
