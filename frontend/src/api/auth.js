import api from "./api";

// LOGIN
export const loginUser = async (data) => {
  const res = await api.post("/login", data);
  return res.data;
};

// SIGNUP
export const signupUser = async (data) => {
  const res = await api.post("/signup", data);
  return res.data;
};

export const requestPasswordReset = (data) =>
    api.post("/forgot-password/request", data);
  
  export const verifyPasswordReset = (data) =>
    api.post("/forgot-password/verify", data);