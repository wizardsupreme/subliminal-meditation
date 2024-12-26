// Make auth functions available globally
window.signInWithGoogle = async function() {
    const provider = new firebase.auth.GoogleAuthProvider();
    try {
        const result = await auth.signInWithPopup(provider);
        const idToken = await result.user.getIdToken();
        window.location.href = `/auth/callback?id_token=${idToken}`;
    } catch (error) {
        console.error("Error during authentication:", error);
    }
}; 