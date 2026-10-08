import { Navigate, Route, Routes } from "react-router-dom";

import Login from "./pages/Login";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import KnowledgeBase from "./pages/KnowledgeBase";
import Investigation from "./pages/Investigation";
import Report from "./pages/Report";

function Guard({ children }) {
    const authenticated =
        localStorage.getItem("eakos_auth") === "true";

    if (!authenticated) {
        return <Navigate to="/login" replace />;
    }

    return children;
}

export default function App() {
    return (
        <Routes>

            {/* LOGIN */}
            <Route
                path="/login"
                element={<Login />}
            />

            {/* DEFAULT */}
            <Route
                path="/"
                element={
                    <Navigate
                        to="/dashboard"
                        replace
                    />
                }
            />

            {/* APPLICATION */}
            <Route
                element={
                    <Guard>
                        <Layout />
                    </Guard>
                }
            >
                <Route
                    path="/dashboard"
                    element={<Dashboard />}
                />

                <Route
                    path="/knowledge-base"
                    element={<KnowledgeBase />}
                />

                <Route
                    path="/investigation"
                    element={<Investigation />}
                />

                <Route
                    path="/report"
                    element={<Report />}
                />

                <Route
                    path="*"
                    element={
                        <Navigate
                            to="/dashboard"
                            replace
                        />
                    }
                />
            </Route>

        </Routes>
    );
}
