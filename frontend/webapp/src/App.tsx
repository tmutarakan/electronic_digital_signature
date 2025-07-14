export const App = () => {
  const ideas = [
    { nick: "cool-idea-nick-1", title: "Idea 1", description: "Description of Idea 1" },
    { nick: "cool-idea-nick-2", title: "Idea 2", description: "Description of Idea 2" },
    { nick: "cool-idea-nick-3", title: "Idea 3", description: "Description of Idea 3" },
    { nick: "cool-idea-nick-4", title: "Idea 4", description: "Description of Idea 4" },
    { nick: "cool-idea-nick-5", title: "Idea 5", description: "Description of Idea 5" },
  ];

  return (
    <div>
      <h1>Ideanick</h1>
      <div>
        {ideas.map((idea) => (
          <div key={idea.nick}>
            <h2>{idea.title}</h2>
            <p>{idea.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};