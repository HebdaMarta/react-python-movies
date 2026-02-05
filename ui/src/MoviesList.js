import MovieListItem from "./MovieListItem";

export default function MoviesList(props) {
    return (
        <div>
            <h2>Movies</h2>
            <ul className="movies-list">
               {props.movies.map((movie, index) => (
                    <li key={movie.id || movie.title}>
                    <MovieListItem
                        movie={movie}
                        index={index}
                        onDelete={() => props.onDeleteMovie(movie)}
                    />
                    </li>
                ))}
            </ul>
        </div>
    );
}
