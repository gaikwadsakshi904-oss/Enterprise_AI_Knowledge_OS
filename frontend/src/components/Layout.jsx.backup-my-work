import { NavLink, Outlet, useNavigate } from "react-router-dom";

const navigation = [
    {
        path: "/dashboard",
        label: "Dashboard",
        icon: "⌂",
    },
    {
        path: "/knowledge-base",
        label: "Knowledge Base",
        icon: "▣",
    },
    {
        path: "/investigation",
        label: "Investigation",
        icon: "⌕",
    },
    {
        path: "/report",
        label: "Reports",
        icon: "▤",
    },
];

export default function Layout() {

    const navigate = useNavigate();

    function logout() {
        localStorage.removeItem("eakos_auth");
        navigate("/login");
    }

    return (
        <div className="shell">

            {/* SIDEBAR */}
            <aside>

                <div className="brand">

                    <div className="brand-logo">
                        E
                    </div>

                    <div>
                        <strong>EAKOS</strong>
                        <small>
                            Enterprise AI OS
                        </small>
                    </div>

                </div>

                <div className="workspace-title">
                    WORKSPACE
                </div>

                <nav>

                    {navigation.map((item) => (

                        <NavLink
                            key={item.path}
                            to={item.path}
                            className={({ isActive }) =>
                                isActive ? "active" : ""
                            }
                        >

                            <span className="nav-icon">
                                {item.icon}
                            </span>

                            <span>
                                {item.label}
                            </span>

                        </NavLink>

                    ))}

                </nav>

                <div className="side-bottom">

                    <div className="secure">

                        <div>
                            <span className="status-dot" />
                            Security posture
                        </div>

                        <small>
                            Monitoring active
                        </small>

                    </div>

                    <button
                        type="button"
                        onClick={logout}
                    >
                        Sign out
                    </button>

                </div>

            </aside>

            {/* MAIN */}
            <main>

                <header>

                    <div>

                        <small>
                            ENTERPRISE INTELLIGENCE
                        </small>

                        <h1>
                            Knowledge Operations Center
                        </h1>

                    </div>

                    <div className="online">

                        <span className="status-dot" />

                        AI services online

                        <b>
                            SK
                        </b>

                    </div>

                </header>

                <section className="content">
                    <Outlet />
                </section>

            </main>

        </div>
    );
}
