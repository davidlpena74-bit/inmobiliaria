/**
 * Weperty Search Suggestions
 * Handles the autocomplete for the main search bar
 */

class SearchSuggestions {
    constructor(inputId, containerId, dbClient) {
        this.input = document.getElementById(inputId);
        this.container = document.getElementById(containerId);
        this.db = dbClient;
        this.debounceTimer = null;
        this.selectedIndex = -1;
        this.suggestions = [];

        if (this.input && this.container) {
            this.init();
        }
    }

    init() {
        this.input.setAttribute('autocomplete', 'off');
        
        this.input.addEventListener('input', () => {
            clearTimeout(this.debounceTimer);
            this.debounceTimer = setTimeout(() => this.handleInput(), 300);
        });

        this.input.addEventListener('keydown', (e) => this.handleKeydown(e));
        
        // Close on blur (with delay to allow click)
        this.input.addEventListener('blur', () => {
            setTimeout(() => this.hide(), 200);
        });

        this.input.addEventListener('focus', () => {
            if (this.input.value.length >= 2) {
                this.show();
            }
        });
    }

    async handleInput() {
        const query = this.input.value.trim();
        if (query.length < 2) {
            this.hide();
            return;
        }

        try {
            const results = await this.fetchSuggestions(query);
            this.suggestions = results;
            this.render();
            if (results.length > 0) {
                this.show();
            } else {
                this.hide();
            }
        } catch (error) {
            console.error('Error fetching suggestions:', error);
        }
    }

    async fetchSuggestions(query) {
        // 1. Fetch Municipalities
        const { data: municipios, error: munError } = await this.db
            .from('inm_municipios')
            .select('id, nombre')
            .ilike('nombre', `%${query}%`)
            .limit(5);

        // 2. Fetch Zones/Districts (Grouped via JS for simplicity if no RPC)
        const { data: props, error: propError } = await this.db
            .from('inm_propiedades')
            .select('zona, municipio_id')
            .ilike('zona', `%${query}%`)
            .eq('estado_publicacion', 'Activo')
            .limit(50);

        let results = [];

        // Add Municipalities to results
        if (municipios) {
            for (const m of municipios) {
                // Get count for this municipality
                const { count } = await this.db
                    .from('inm_propiedades')
                    .select('*', { count: 'exact', head: true })
                    .eq('municipio_id', m.id)
                    .eq('estado_publicacion', 'Activo');

                results.push({
                    id: m.id,
                    name: m.nombre,
                    type: 'Municipio',
                    count: count || 0,
                    filterKey: 'municipio_id',
                    filterValue: m.id
                });
            }
        }

        // Add Unique Zones to results
        if (props) {
            const uniqueZones = {};
            props.forEach(p => {
                if (p.zona && !uniqueZones[p.zona]) {
                    uniqueZones[p.zona] = {
                        name: p.zona,
                        municipio_id: p.municipio_id,
                        count: props.filter(x => x.zona === p.zona).length
                    };
                }
            });

            for (const zoneName in uniqueZones) {
                // Check if we already have this as a municipality
                if (results.some(r => r.name === zoneName)) continue;

                results.push({
                    name: zoneName,
                    type: 'Distrito',
                    count: uniqueZones[zoneName].count,
                    filterKey: 'zona',
                    filterValue: zoneName
                });
            }
        }

        return results.sort((a, b) => b.count - a.count).slice(0, 10);
    }

    render() {
        const query = this.input.value;
        this.container.innerHTML = '';
        this.selectedIndex = -1;

        this.suggestions.forEach((item, index) => {
            const div = document.createElement('div');
            div.className = 'suggestion-item';
            div.dataset.index = index;
            
            // Highlight match
            const highlightedName = item.name.replace(
                new RegExp(`(${this.escapeRegExp(query)})`, 'gi'), 
                '<b>$1</b>'
            );

            div.innerHTML = `
                <div class="suggestion-content">
                    <span class="suggestion-title">${highlightedName}</span>
                    <span class="suggestion-subtitle">
                        <i class="fa-regular fa-circle-dot"></i> ${item.type}
                    </span>
                </div>
                <div class="suggestion-count">${item.count}</div>
            `;

            div.addEventListener('click', () => this.selectItem(item));
            this.container.appendChild(div);
        });
    }

    escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    handleKeydown(e) {
        const items = this.container.querySelectorAll('.suggestion-item');
        if (!this.isVisible() || items.length === 0) return;

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            this.selectedIndex = (this.selectedIndex + 1) % items.length;
            this.updateSelection(items);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            this.selectedIndex = (this.selectedIndex - 1 + items.length) % items.length;
            this.updateSelection(items);
        } else if (e.key === 'Enter') {
            if (this.selectedIndex > -1) {
                e.preventDefault();
                this.selectItem(this.suggestions[this.selectedIndex]);
            }
        } else if (e.key === 'Escape') {
            this.hide();
        }
    }

    updateSelection(items) {
        items.forEach((item, index) => {
            item.classList.toggle('selected', index === this.selectedIndex);
        });
        if (this.selectedIndex > -1) {
            items[this.selectedIndex].scrollIntoView({ block: 'nearest' });
        }
    }

    selectItem(item) {
        this.input.value = item.name;
        this.hide();
        
        // Execute search or redirect
        const mode = typeof currentSearchMode !== 'undefined' ? currentSearchMode : 'buy';
        window.location.href = `inmuebles.html?mode=${mode}&${item.filterKey}=${encodeURIComponent(item.filterValue)}`;
    }

    show() {
        this.container.classList.add('active');
    }

    hide() {
        this.container.classList.remove('active');
    }

    isVisible() {
        return this.container.classList.contains('active');
    }
}

// Auto-initialize when Supabase is available
document.addEventListener('DOMContentLoaded', () => {
    console.log("SearchSuggestions: DOM Loaded, checking for DB...");
    let attempts = 0;
    const checkInterval = setInterval(() => {
        attempts++;
        if (window.db || typeof db !== 'undefined') {
            clearInterval(checkInterval);
            const supabaseClient = window.db || db;
            console.log("SearchSuggestions: DB found, initializing...");
            new SearchSuggestions('mainSearch', 'searchSuggestions', supabaseClient);
        } else if (attempts > 50) {
            clearInterval(checkInterval);
            console.error("SearchSuggestions: Supabase client (db) not found after 5 seconds.");
        }
    }, 100);
});
