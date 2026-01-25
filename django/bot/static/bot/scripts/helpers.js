export async function handleRequest(headers_content, body_content) {
  try {
    const apiEndpont = "/get_response/";
    // const apiEndpont = "http://localhost:8000/api/get_response/";

    // const apiEndpont = "http://13.50.248.208/api/get_response/";
    // const apiEndpont = "http://localhost/api/get_response/";
    const res = await fetch(apiEndpont, {
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

export const getLocation = () => {
  return new Promise((resolve, reject) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) =>
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          }),
        (error) => reject(error),
      );
    } else {
      reject(new Error("Geolocation not supported"));
    }
  });
};
