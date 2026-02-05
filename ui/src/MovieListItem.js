export default function MovieListItem(props) {
    const { movie, onDelete } = props;

    return (
        <div className="movie-card" style={{ animationDelay: `${props.index * 0.1}s` }}>
            <div>
                <strong>{movie.title}</strong>{' '}
                <span>({movie.year})</span>{' '}
                directed by {movie.director}{' '}
                <button className="delete-btn" onClick={onDelete}>
                Delete
                </button>
            </div>

            <div>{movie.description}</div>

            {movie.actors && movie.actors.length > 0 && (
                <div>
                    <strong>Actors:</strong>
                    <ul>
                        {movie.actors.map((actor, idx) => (
                            <li key={idx}>{actor}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}