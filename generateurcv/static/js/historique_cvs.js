function chargerHistoriqueCVs() {
    fetch('/historique_cvs/')
        .then(response => {
            console.log(">> Réponse brute :", response);
            return response.json();
        })
        .then(data => {
            console.log(">> Données JSON reçues :", data);

            if (!data.success) throw new Error(data.message || 'Réponse invalide');

            const container = document.getElementById('documents-list');
            container.innerHTML = '';

            data.cvs.forEach(cv => {
                const div = document.createElement('div');
                div.className = 'flex items-center justify-between border-b px-4 py-3 hover:bg-gray-50';

                div.innerHTML = `
                    <div class="flex items-center gap-4">
                        <img src="${cv.preview_image}" alt="aperçu" class="w-16 h-16 object-cover rounded shadow" />
                        <div>
                            <p class="font-semibold text-gray-800">${cv.titre}</p>
                            <p class="text-sm text-gray-500">Créé le ${cv.date}</p>
                        </div>
                    </div>
                    <div>
                        <a href="#" onclick="chargerCV(${cv.id})" class="text-blue-600 hover:underline text-sm">Voir CV</a>
                    </div>
                `;

                container.appendChild(div);
            });
        })
        .catch(err => {
            console.error('❌ Erreur JS lors du fetch /historique_cvs/ :', err);
            alert('Erreur lors du chargement de l’historique.');
        });
}

function chargerCV(id) {
    fetch(`/api/cv/${id}/`)
        .then(response => response.json())
        .then(data => {
            if (!data.success) throw new Error(data.message || 'Impossible de charger le CV.');

            document.getElementById('fullName').value = data.cv.full_name;
            document.getElementById('title').value = data.cv.title;
            document.getElementById('email').value = data.cv.email;
            document.getElementById('phone').value = data.cv.phone;
            document.getElementById('summary').value = data.cv.summary;

            if (data.cv.photo) {
                document.getElementById('photo-preview').innerHTML = `
                    <img src="${data.cv.photo}" class="w-full h-full object-cover" />
                `;
            }

            const expList = document.getElementById('experience-list');
            expList.innerHTML = '';
            data.experiences.forEach(exp => {
                expList.innerHTML += `
                    <div class="p-2 bg-gray-50 rounded mb-2">
                        <p class="font-semibold">${exp.position} @ ${exp.company}</p>
                        <p class="text-sm text-gray-500">${exp.date}</p>
                        <p class="text-sm">${exp.description}</p>
                    </div>
                `;
            });

            const eduList = document.getElementById('education-list');
            eduList.innerHTML = '';
            data.education.forEach(edu => {
                eduList.innerHTML += `
                    <div class="p-2 bg-gray-50 rounded mb-2">
                        <p class="font-semibold">${edu.degree} à ${edu.institution}</p>
                        <p class="text-sm text-gray-500">${edu.date}</p>
                        <p class="text-sm">${edu.description}</p>
                    </div>
                `;
            });

            const skillList = document.getElementById('skills-list');
            skillList.innerHTML = '';
            data.skills.forEach(skill => {
                skillList.innerHTML += `
                    <div class="p-2 bg-gray-50 rounded mb-2">
                        <p class="text-sm">${skill.name} (Niveau ${skill.level})</p>
                    </div>
                `;
            });

            const langList = document.getElementById('languages-list');
            langList.innerHTML = '';
            data.languages.forEach(lang => {
                langList.innerHTML += `
                    <div class="p-2 bg-gray-50 rounded mb-2">
                        <p class="text-sm">${lang.name} (${lang.level})</p>
                    </div>
                `;
            });

            const interestList = document.getElementById('interests-list');
            interestList.innerHTML = '';
            data.interests.forEach(item => {
                interestList.innerHTML += `
                    <div class="p-2 bg-gray-50 rounded mb-2">
                        <p class="text-sm">${item.name}</p>
                    </div>
                `;
            });

            // Affiche le formulaire
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.add('hidden'));
            document.getElementById('personal').classList.remove('hidden');
        })
        .catch(err => {
            console.error('❌ Erreur chargement CV :', err);
            alert('Erreur lors du chargement du CV.');
        });
}

document.addEventListener('DOMContentLoaded', () => {
    chargerHistoriqueCVs();
});
