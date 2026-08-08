import {
  Search,
  FileText
} from "lucide-react";

function SearchPage() {

  return (
    <div>

      <div className="page-title">

        <div>

          <h1>Semantic Search</h1>

          <p>
            Search your knowledge using AI-powered semantic understanding.
          </p>

        </div>

      </div>


      <div className="semantic-search">

        <Search size={20} />

        <input
          placeholder="Search your enterprise knowledge..."
        />

        <button>
          Search
        </button>

      </div>


      <div className="search-results">

        <div className="search-result">

          <FileText size={20} />

          <div>

            <h3>
              Enterprise Strategy 2026
            </h3>

            <p>
              Relevant information about the company's
              strategic objectives and business plans.
            </p>

          </div>

        </div>


        <div className="search-result">

          <FileText size={20} />

          <div>

            <h3>
              Employee Handbook
            </h3>

            <p>
              Relevant policies, employee guidelines
              and organizational procedures.
            </p>

          </div>

        </div>

      </div>

    </div>
  );
}

export default SearchPage;